"""Outcome ledger and learner for the Upwork pipeline.

One row per submitted proposal: the decisions that produced it and what happened. Claude does the
Upwork MCP calls; this script does every piece of arithmetic and every weight change, so learning
is deterministic and bounded rather than improvised per session.

Usage:
  python outcomes.py add    '<json row>'            append a proposal (rejects duplicates, bad enums)
  python outcomes.py update <proposal_id> '<json>'  merge fields into an existing row
  python outcomes.py due                            proposals whose status needs a refresh
  python outcomes.py status                         is a sync / learning pass due? (JSON)
  python outcomes.py mark-sync                      record that a sync just finished
  python outcomes.py gaps                           rows missing the tags learning needs
  python outcomes.py summary [--json]               breakdowns with sample-size guards
  python outcomes.py learn [--apply]                observations, calibration proposals, version check
"""

import csv
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
SKILLS_ROOT = SKILL.parent
DATA = SKILL / "data" / "outcomes.csv"
STATE = SKILL / "data" / "state.json"
OBSERVATIONS = SKILL / "references" / "observations.md"
CAL_LOG = SKILL / "references" / "calibration-log.md"
WEIGHTS = SKILLS_ROOT / "job-scout" / "references" / "learned-weights.json"

FIELDS = [
    # identity
    "proposal_id", "job_id", "title", "submitted_at_utc",
    # decisions (written at submit, never changed afterwards)
    "cohort", "rule_version", "scout_score", "match_pct",
    "comp_match", "comp_client", "comp_winnability", "comp_competition", "comp_rate", "comp_post",
    "wedge_type", "mode", "contract_type", "bid", "connects_cost", "boosted", "boost_connects",
    "proposals_at_submit", "client_spend", "client_hires",
    # outcome (refreshed daily)
    "status", "client_messaged", "field_total", "field_opened", "field_shortlisted",
    "field_messaged", "first_signal_at_utc", "last_checked_utc", "notes",
]
COMPONENTS = ["match", "client", "winnability", "competition", "rate", "post"]
WEDGE_TYPES = ["impossible_spec", "misdiagnosis", "unstated_failure", "wrong_tool",
               "buried_real_project", "scope_trap", "none"]
REQUIRED_TAGS = ["scout_score", "match_pct", "wedge_type", "bid", "connects_cost"]

TERMINAL = {"hired", "declined", "closed", "withdrawn"}
ENGAGED = {"engaged", "offered", "hired"}
# Outcomes that say something about the letter. Pending, dead, closed and withdrawn do not.
JUDGED = ENGAGED | {"declined", "passed_over", "no_response"}

# Sample-size discipline (Hashim, 2026-09-14): 30-50 results before scoring changes mean anything.
MIN_BUCKET = 8          # a bucket below this is never acted on
STAGE_CALIBRATE = 30    # below: observations only
STAGE_CONFIDENT = 50    # from here, small lean adjustments are allowed too
STRONG_STEP = 3         # max points moved per value when confidence intervals separate
LEAN_STEP = 1           # max points moved per value on a lean signal (confident stage only)
MIN_DAYS_BETWEEN_APPLY = 7
REVERT_MIN_JUDGED = 15
Z90 = 1.645

DEAD_AFTER_H = 24
PASSED_OVER_AFTER_H = 72
NO_RESPONSE_AFTER_D = 7
SYNC_EVERY_H = 20
LEARN_EVERY_H = 24


# ---------------------------------------------------------------- basics

def parse_ts(value):
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def fmt_ts(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def load():
    if not DATA.exists():
        return []
    with DATA.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save(rows):
    DATA.parent.mkdir(parents=True, exist_ok=True)
    with DATA.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in FIELDS})


def load_json(path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


_REFERENCE = None


def now():
    """Reference time. This machine's clock has run ~12h behind Upwork's timestamps (seen
    2026-09-14), which silently mislabels proposal ages. Use the later of the local clock and the
    newest last_checked_utc, which is written from API time."""
    global _REFERENCE
    if _REFERENCE is None:
        checked = [parse_ts(r.get("last_checked_utc")) for r in load()]
        _REFERENCE = max([datetime.now(timezone.utc)] + [c for c in checked if c])
    return _REFERENCE


def num(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def outcome(row):
    """One label per row, strongest signal first."""
    status = (row.get("status") or "").lower()
    if status == "hired":
        return "hired"
    if status == "offered":
        return "offered"
    if row.get("client_messaged") == "yes" or status == "activated":
        return "engaged"
    if status == "declined":
        return "declined"
    if status == "withdrawn":
        return "withdrawn"
    if status == "archived":
        return "closed"
    submitted = parse_ts(row.get("submitted_at_utc"))
    age = now() - submitted if submitted else None
    if age and age > timedelta(hours=DEAD_AFTER_H) and num(row.get("field_opened")) == 0:
        return "dead"
    messaged = num(row.get("field_messaged"))
    if age and age > timedelta(hours=PASSED_OVER_AFTER_H) and messaged and messaged > 0:
        return "passed_over"   # client is talking to others, not us: read and lost, most likely
    if age and age > timedelta(days=NO_RESPONSE_AFTER_D):
        return "no_response"
    return "pending"


def wilson(k, n, z=Z90):
    """90% Wilson interval. Honest at the tiny n this pipeline lives with."""
    if n == 0:
        return 0.0, 1.0
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / denom
    return max(0.0, centre - half), min(1.0, centre + half)


def stage_for(judged):
    if judged < STAGE_CALIBRATE:
        return "observe"
    if judged < STAGE_CONFIDENT:
        return "calibrate"
    return "confident"


# ---------------------------------------------------------------- ledger commands

def cmd_add(payload):
    row = json.loads(payload)
    unknown = set(row) - set(FIELDS)
    if unknown:
        sys.exit(f"unknown fields: {sorted(unknown)}")
    if row.get("wedge_type") and row["wedge_type"] not in WEDGE_TYPES:
        sys.exit(f"wedge_type must be one of {WEDGE_TYPES}")
    rows = load()
    if any(r["proposal_id"] == str(row.get("proposal_id")) for r in rows):
        sys.exit(f"duplicate proposal_id {row.get('proposal_id')}")
    rows.append({k: str(v) for k, v in row.items()})
    save(rows)
    missing = [t for t in REQUIRED_TAGS if not str(row.get(t, "")).strip()]
    print(f"added {row['proposal_id']}" + (f"  WARNING untagged: {missing}" if missing else ""))


def cmd_update(proposal_id, payload):
    changes = json.loads(payload)
    unknown = set(changes) - set(FIELDS)
    if unknown:
        sys.exit(f"unknown fields: {sorted(unknown)}")
    rows = load()
    for row in rows:
        if row["proposal_id"] == proposal_id:
            before = outcome(row)
            row.update({k: str(v) for k, v in changes.items()})
            after = outcome(row)
            if after in ENGAGED and before not in ENGAGED and not row.get("first_signal_at_utc"):
                row["first_signal_at_utc"] = fmt_ts(now())
            save(rows)
            flag = "  <-- NEW SIGNAL" if after in ENGAGED and before not in ENGAGED else ""
            print(f"updated {proposal_id}: {before} -> {after}{flag}")
            return
    sys.exit(f"no row for {proposal_id}")


def due_rows():
    cutoff = now() - timedelta(hours=SYNC_EVERY_H)
    out = []
    for row in load():
        if outcome(row) in TERMINAL:
            continue
        checked = parse_ts(row.get("last_checked_utc"))
        if checked is None or checked < cutoff:
            out.append(row)
    return out


def cmd_due():
    for row in due_rows():
        print(row["proposal_id"], row["title"][:60])


def cmd_status():
    state = load_json(STATE, {})
    last_learn = parse_ts(state.get("last_learn_utc"))
    print(json.dumps({
        "sync_due": bool(due_rows()),
        "learn_due": last_learn is None or now() - last_learn > timedelta(hours=LEARN_EVERY_H),
        "last_sync_utc": state.get("last_sync_utc"),
        "last_learn_utc": state.get("last_learn_utc"),
        "last_apply_utc": state.get("last_apply_utc"),
    }, indent=2))


def cmd_mark_sync():
    state = load_json(STATE, {})
    state["last_sync_utc"] = fmt_ts(now())
    save_json(STATE, state)
    print("sync marked", state["last_sync_utc"])


def cmd_gaps():
    for row in load():
        missing = [t for t in REQUIRED_TAGS if not (row.get(t) or "").strip()]
        if missing:
            print(row["proposal_id"], row["title"][:45], "missing:", ",".join(missing))


# ---------------------------------------------------------------- summary

def stats(rows):
    labels = [outcome(r) for r in rows]
    judged = [l for l in labels if l in JUDGED]
    engaged = sum(l in ENGAGED for l in labels)
    connects = sum((num(r.get("connects_cost")) or 0) + (num(r.get("boost_connects")) or 0) for r in rows)
    lo, hi = wilson(engaged, len(judged))
    return {
        "n": len(rows), "judged": len(judged), "engaged": engaged,
        "passed_over": labels.count("passed_over"), "dead": labels.count("dead"),
        "closed": labels.count("closed"), "pending": labels.count("pending"),
        "hired": labels.count("hired"),
        "engaged_rate": round(engaged / len(judged), 3) if judged else None,
        "ci90": [round(lo, 2), round(hi, 2)],
        "connects": int(connects),
        "connects_missing": sum(num(r.get("connects_cost")) is None for r in rows),
        "connects_per_engaged": round(connects / engaged, 1) if engaged else None,
    }


def score_band(row):
    s = num(row.get("scout_score"))
    if s is None:
        return "unscored"
    return "80+" if s >= 80 else "65-79" if s >= 65 else "<65"


def rate_band(row):
    if row.get("contract_type") != "hourly":
        return "fixed"
    b = num(row.get("bid"))
    if b is None:
        return "unknown"
    return "$65+" if b >= 65 else "$50-64" if b >= 50 else "<$50"


def group(rows, key):
    buckets = {}
    for row in rows:
        buckets.setdefault(key(row), []).append(row)
    return {k: stats(v) for k, v in sorted(buckets.items())}


DIMENSIONS = [
    ("COHORT", lambda r: r.get("cohort") or "unknown"),
    ("WEDGE TYPE", lambda r: r.get("wedge_type") or "untagged"),
    ("SCOUT SCORE", score_band),
    ("RATE", rate_band),
    ("BOOSTED", lambda r: r.get("boosted") or "unknown"),
    ("RULE VERSION", lambda r: r.get("rule_version") or "unknown"),
]


def cmd_summary(as_json):
    rows = load()
    overall = stats(rows)
    stage = stage_for(overall["judged"])
    report = {"generated_utc": fmt_ts(now()), "stage": stage, "overall": overall,
              "groups": {name: group(rows, key) for name, key in DIMENSIONS},
              "rows": [{"proposal_id": r["proposal_id"], "title": r["title"][:50], "outcome": outcome(r)}
                       for r in rows]}
    if as_json:
        print(json.dumps(report, indent=2))
        return

    def line(name, s):
        rate = f"{s['engaged_rate']:.0%}" if s["engaged_rate"] is not None else "n/a"
        ci = f"[{s['ci90'][0]:.0%}-{s['ci90'][1]:.0%}]" if s["judged"] else ""
        small = " (n<8)" if s["judged"] < MIN_BUCKET else ""
        miss = f" ({s['connects_missing']} unrecorded)" if s["connects_missing"] else ""
        return (f"  {name:<22} n={s['n']:<3} judged={s['judged']:<3} engaged={s['engaged']:<2} "
                f"passed_over={s['passed_over']:<2} dead={s['dead']:<2} rate={rate} {ci}{small} "
                f"connects={s['connects']}{miss}")

    print(f"OUTCOMES  {report['generated_utc']}  stage={stage} "
          f"(observe <{STAGE_CALIBRATE} judged, confident >={STAGE_CONFIDENT})")
    print(line("overall", overall))
    for name, _ in DIMENSIONS:
        print(name)
        for bucket, s in report["groups"][name].items():
            print(line(bucket, s))
    print("ROWS")
    for r in report["rows"]:
        print(f"  {r['proposal_id']}  {r['outcome']:<11} {r['title']}")


# ---------------------------------------------------------------- learning

def clamp(value, base):
    if base == 0:
        return max(0.0, min(3.0, value))
    return max(0.5 * base, min(1.5 * base, value))


def wedge_recommendations(judged_rows, stage):
    """Compare each wedge type against all other judged letters."""
    recs, table = [], {}
    for wedge in WEDGE_TYPES:
        inside = [r for r in judged_rows if (r.get("wedge_type") or "") == wedge]
        rest = [r for r in judged_rows if (r.get("wedge_type") or "") != wedge]
        k_in, n_in = sum(outcome(r) in ENGAGED for r in inside), len(inside)
        k_out, n_out = sum(outcome(r) in ENGAGED for r in rest), len(rest)
        if n_in == 0:
            continue
        ci_in, ci_out = wilson(k_in, n_in), wilson(k_out, n_out)
        table[wedge] = {"judged": n_in, "engaged": k_in, "rate": round(k_in / n_in, 2),
                        "ci90": [round(ci_in[0], 2), round(ci_in[1], 2)],
                        "rest_rate": round(k_out / n_out, 2) if n_out else None}
        if stage == "observe" or n_in < MIN_BUCKET or n_out < MIN_BUCKET:
            continue
        diff = k_in / n_in - k_out / n_out
        if ci_in[0] > ci_out[1]:
            recs.append({"kind": "wedge_points", "key": wedge, "delta": STRONG_STEP, "tier": "strong",
                         "evidence": table[wedge]})
        elif ci_in[1] < ci_out[0]:
            recs.append({"kind": "wedge_points", "key": wedge, "delta": -STRONG_STEP, "tier": "strong",
                         "evidence": table[wedge]})
        elif stage == "confident" and abs(diff) >= 0.15:
            recs.append({"kind": "wedge_points", "key": wedge, "delta": LEAN_STEP if diff > 0 else -LEAN_STEP,
                         "tier": "lean", "evidence": table[wedge]})
    return recs, table


def component_recommendations(judged_rows, stage):
    """Does each scout component actually separate engaged letters from the rest?
    Needs the comp_* fractions (0-1) the scout records from 2026-09-14 on."""
    tagged = [r for r in judged_rows if all(num(r.get(f"comp_{c}")) is not None for c in COMPONENTS)]
    engaged = [r for r in tagged if outcome(r) in ENGAGED]
    other = [r for r in tagged if outcome(r) not in ENGAGED]
    report = {"tagged_judged": len(tagged), "engaged": len(engaged), "not_engaged": len(other)}
    recs = []
    if len(engaged) < MIN_BUCKET or len(other) < MIN_BUCKET:
        return recs, report
    for c in COMPONENTS:
        mean_e = sum(num(r[f"comp_{c}"]) for r in engaged) / len(engaged)
        mean_o = sum(num(r[f"comp_{c}"]) for r in other) / len(other)
        diff = mean_e - mean_o
        report[c] = round(diff, 3)
        if stage == "observe":
            continue
        if abs(diff) >= 0.20:
            recs.append({"kind": "component", "key": c, "delta": 2 if diff > 0 else -2, "tier": "strong",
                         "evidence": {"engaged_mean": round(mean_e, 2), "other_mean": round(mean_o, 2)}})
        elif stage == "confident" and abs(diff) >= 0.10:
            recs.append({"kind": "component", "key": c, "delta": LEAN_STEP if diff > 0 else -LEAN_STEP,
                         "tier": "lean", "evidence": {"engaged_mean": round(mean_e, 2), "other_mean": round(mean_o, 2)}})
    return recs, report


def scout_predictiveness(judged_rows):
    scored = [r for r in judged_rows if num(r.get("scout_score")) is not None]
    e = [num(r["scout_score"]) for r in scored if outcome(r) in ENGAGED]
    o = [num(r["scout_score"]) for r in scored if outcome(r) not in ENGAGED]
    return {"scored_judged": len(scored),
            "engaged_mean_score": round(sum(e) / len(e), 1) if e else None, "engaged_n": len(e),
            "other_mean_score": round(sum(o) / len(o), 1) if o else None, "other_n": len(o)}


def version_check(rows):
    """Newest rule_version group vs the one before it, by first submission time."""
    groups = {}
    for r in rows:
        v = r.get("rule_version") or "unknown"
        t = parse_ts(r.get("submitted_at_utc"))
        g = groups.setdefault(v, {"first": t, "rows": []})
        g["rows"].append(r)
        if t and (g["first"] is None or t < g["first"]):
            g["first"] = t
    # Order by the latest submission in each group (the version most recently in use comes last),
    # with the version name as a tie-break so equal timestamps can never flip the comparison.
    for g in groups.values():
        times = [parse_ts(r.get("submitted_at_utc")) for r in g["rows"]]
        g["last"] = max([t for t in times if t] or [datetime.min.replace(tzinfo=timezone.utc)])
    ordered = sorted(groups.items(), key=lambda kv: (kv[1]["last"], kv[0]))
    if len(ordered) < 2:
        return {"verdict": "only one rule version so far"}
    (prev_v, prev), (new_v, new) = ordered[-2], ordered[-1]
    sp, sn = stats(prev["rows"]), stats(new["rows"])
    result = {"previous": prev_v, "previous_judged": sp["judged"], "previous_rate": sp["engaged_rate"],
              "newest": new_v, "newest_judged": sn["judged"], "newest_rate": sn["engaged_rate"]}
    if sn["judged"] < REVERT_MIN_JUDGED or sp["judged"] < REVERT_MIN_JUDGED:
        result["verdict"] = f"too early (needs {REVERT_MIN_JUDGED} judged in both)"
    elif sn["ci90"][1] < sp["ci90"][0]:
        result["verdict"] = "REVERT CANDIDATE: newest rules clearly worse"
    elif (sp["engaged_rate"] or 0) - (sn["engaged_rate"] or 0) >= 0.10:
        result["verdict"] = "WATCH: newest rules trending worse, not yet significant"
    else:
        result["verdict"] = "no regression"
    return result


def apply_recommendations(recs):
    weights = load_json(WEIGHTS, None)
    if weights is None:
        sys.exit(f"missing {WEIGHTS}")
    base, cur = weights["baseline"], weights["current"]
    changes = []
    for rec in recs:
        if rec["kind"] == "wedge_points":
            old = cur["wedge_points"][rec["key"]]
            new = round(clamp(old + rec["delta"], base["wedge_points"][rec["key"]]), 1)
            if new != old:
                cur["wedge_points"][rec["key"]] = new
                changes.append(f"wedge_points.{rec['key']} {old} -> {new} ({rec['tier']})")
        else:
            old = cur["components"][rec["key"]]
            new = clamp(old + rec["delta"], base["components"][rec["key"]])
            cur["components"][rec["key"]] = new
            changes.append(f"components.{rec['key']} {old} -> {new} ({rec['tier']}, before renormalising)")
    total = sum(cur["components"].values())
    cur["components"] = {k: round(v * 100 / total, 1) for k, v in cur["components"].items()}
    cur["wedge_preference"] = sorted(WEDGE_TYPES, key=lambda w: -cur["wedge_points"][w])
    weights["updated_utc"] = fmt_ts(now())
    weights["history"].append({"applied_utc": weights["updated_utc"], "changes": changes,
                               "recommendations": recs})
    save_json(WEIGHTS, weights)
    return changes


def cmd_learn(apply):
    rows = load()
    judged_rows = [r for r in rows if outcome(r) in JUDGED]
    overall = stats(rows)
    stage = stage_for(len(judged_rows))
    wedge_recs, wedge_table = wedge_recommendations(judged_rows, stage)
    comp_recs, comp_report = component_recommendations(judged_rows, stage)
    recs = wedge_recs + comp_recs
    predict = scout_predictiveness(judged_rows)
    versions = version_check(rows)
    passed_over = [r for r in rows if outcome(r) == "passed_over"]
    state = load_json(STATE, {})

    applied, blocked = [], None
    if apply and recs:
        last = parse_ts(state.get("last_apply_utc"))
        if stage == "observe":
            blocked = "stage=observe"
        elif last and now() - last < timedelta(days=MIN_DAYS_BETWEEN_APPLY):
            blocked = f"last apply {state['last_apply_utc']}, minimum {MIN_DAYS_BETWEEN_APPLY} days"
        else:
            applied = apply_recommendations(recs)
            state["last_apply_utc"] = fmt_ts(now())

    print(f"LEARN  {fmt_ts(now())}  stage={stage}  judged={len(judged_rows)}  engaged={overall['engaged']}  "
          f"rate={overall['engaged_rate']}  ci90={overall['ci90']}")
    if stage == "observe":
        print(f"  Observation only: {STAGE_CALIBRATE - len(judged_rows)} more judged proposals before any "
              f"results-based change is allowed.")
    print("WEDGE TYPE (vs all other judged letters)")
    for w, t in wedge_table.items():
        small = " (n<8, observe)" if t["judged"] < MIN_BUCKET else ""
        print(f"  {w:<20} judged={t['judged']:<3} engaged={t['engaged']} rate={t['rate']:.0%} "
              f"ci90={t['ci90']} rest={t['rest_rate']}{small}")
    print("SCOUT SCORE PREDICTIVENESS", json.dumps(predict))
    print("SCOUT COMPONENTS", json.dumps(comp_report))
    print("VERSION CHECK", json.dumps(versions))
    print("PASSED OVER (read these letters against the engaged ones)")
    for r in passed_over:
        print(f"  {r['proposal_id']}  wedge={r.get('wedge_type') or '?':<20} bid={r.get('bid')} "
              f"score={r.get('scout_score') or '-'}  {r['title'][:50]}")
    print("RECOMMENDATIONS", json.dumps(recs) if recs else "none (guards not met)")
    if apply:
        print("APPLIED", applied if applied else f"nothing ({blocked or 'no recommendations'})")

    # One dated observation entry per day: the durable record of what the data said.
    today = now().strftime("%Y-%m-%d")
    if state.get("last_observation_date") != today:
        OBSERVATIONS.parent.mkdir(parents=True, exist_ok=True)
        lines = [f"\n## {today} — stage {stage}, judged {len(judged_rows)}, engaged {overall['engaged']}\n"]
        for w, t in wedge_table.items():
            lines.append(f"- {w}: {t['engaged']}/{t['judged']} engaged, ci90 {t['ci90']}"
                         f"{' (observe)' if t['judged'] < MIN_BUCKET else ''}")
        lines.append(f"- scout predictiveness: {json.dumps(predict)}")
        lines.append(f"- version check: {versions['verdict']}")
        lines.append(f"- passed over: {len(passed_over)} — " + "; ".join(r['title'][:40] for r in passed_over))
        lines.append(f"- recommendations: {len(recs)}; applied: {applied or 'none'}")
        with OBSERVATIONS.open("a", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        state["last_observation_date"] = today
    if applied:
        with CAL_LOG.open("a", encoding="utf-8") as f:
            f.write(f"\n## {fmt_ts(now())} — stage {stage}, judged {len(judged_rows)}\n"
                    + "\n".join(f"- {c}" for c in applied)
                    + f"\n- evidence: {json.dumps(recs)}\n")
    state["last_learn_utc"] = fmt_ts(now())
    save_json(STATE, state)


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    cmd = args[0]
    if cmd == "add" and len(args) == 2:
        cmd_add(args[1])
    elif cmd == "update" and len(args) == 3:
        cmd_update(args[1], args[2])
    elif cmd == "due":
        cmd_due()
    elif cmd == "status":
        cmd_status()
    elif cmd == "mark-sync":
        cmd_mark_sync()
    elif cmd == "gaps":
        cmd_gaps()
    elif cmd == "summary":
        cmd_summary("--json" in args)
    elif cmd == "learn":
        cmd_learn("--apply" in args)
    else:
        sys.exit(__doc__)
