"""Outcome ledger for the Upwork pipeline.

One row per submitted proposal. Decision fields are written at submit time, outcome fields are
refreshed from the Upwork MCP daily. Claude does the MCP calls; this script does every piece of
arithmetic so no rate is ever computed by hand.

Usage:
  python outcomes.py add    '<json row>'            append a proposal (fails on duplicate id)
  python outcomes.py update <proposal_id> '<json>'  merge fields into an existing row
  python outcomes.py due                            proposals whose outcome needs a refresh
  python outcomes.py summary [--json]               cohort / wedge / score / rate breakdown
"""

import csv
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "outcomes.csv"

FIELDS = [
    # identity
    "proposal_id", "job_id", "title", "submitted_at_utc",
    # decisions (written at submit, never changed afterwards)
    "cohort", "rule_version", "scout_score", "match_pct", "wedge_type", "mode",
    "contract_type", "bid", "connects_cost", "boosted", "boost_connects",
    "proposals_at_submit", "client_spend", "client_hires",
    # outcome (refreshed daily)
    "status", "client_messaged", "field_total", "field_opened", "field_shortlisted",
    "field_messaged", "first_signal_at_utc", "last_checked_utc", "notes",
]

TERMINAL = {"hired", "declined", "closed", "withdrawn"}
MIN_BUCKET = 8    # below this a bucket is "observe", never "act"
MIN_TOTAL = 30    # below this no weight change is allowed at all
DEAD_AFTER_H = 24
PASSED_OVER_AFTER_H = 72
NO_RESPONSE_AFTER_D = 7


_REFERENCE = None


def now():
    """Reference time. The local clock on this machine has run ~12h behind Upwork's timestamps
    (seen 2026-09-14), which silently mislabels proposal ages. Use the later of the local clock
    and the newest last_checked_utc, which is written from API time."""
    global _REFERENCE
    if _REFERENCE is None:
        local = datetime.now(timezone.utc)
        checked = [parse_ts(r.get("last_checked_utc")) for r in load()]
        checked = [c for c in checked if c]
        _REFERENCE = max([local] + checked)
    return _REFERENCE


def parse_ts(value):
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


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


def num(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def outcome(row):
    """Derive one outcome label from the raw fields. Order matters: strongest signal first."""
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
    opened = num(row.get("field_opened"))
    messaged = num(row.get("field_messaged"))
    if age and age > timedelta(hours=DEAD_AFTER_H) and opened == 0:
        return "dead"
    # Client is talking to other applicants and not to us: the letter was likely read and lost.
    # The most useful learning row the API can produce.
    if age and age > timedelta(hours=PASSED_OVER_AFTER_H) and messaged and messaged > 0:
        return "passed_over"
    if age and age > timedelta(days=NO_RESPONSE_AFTER_D):
        return "no_response"
    return "pending"


def cmd_add(payload):
    row = json.loads(payload)
    rows = load()
    if any(r["proposal_id"] == str(row.get("proposal_id")) for r in rows):
        sys.exit(f"duplicate proposal_id {row.get('proposal_id')}")
    unknown = set(row) - set(FIELDS)
    if unknown:
        sys.exit(f"unknown fields: {sorted(unknown)}")
    rows.append({k: str(v) for k, v in row.items()})
    save(rows)
    print(f"added {row['proposal_id']}")


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
            if after != before and after in {"engaged", "offered", "hired"} and not row.get("first_signal_at_utc"):
                row["first_signal_at_utc"] = now().strftime("%Y-%m-%dT%H:%M:%SZ")
            save(rows)
            print(f"updated {proposal_id}: {before} -> {after}")
            return
    sys.exit(f"no row for {proposal_id}")


def cmd_due():
    cutoff = now() - timedelta(hours=20)
    for row in load():
        if outcome(row) in TERMINAL:
            continue
        checked = parse_ts(row.get("last_checked_utc"))
        if checked is None or checked < cutoff:
            print(row["proposal_id"], row["title"][:60])


def score_band(row):
    s = num(row.get("scout_score"))
    if s is None:
        return "unscored"
    if s >= 80:
        return "80+"
    if s >= 65:
        return "65-79"
    return "<65"


def rate_band(row):
    if row.get("contract_type") != "hourly":
        return "fixed"
    b = num(row.get("bid"))
    if b is None:
        return "unknown"
    if b >= 65:
        return "$65+"
    if b >= 50:
        return "$50-64"
    return "<$50"


def stats(rows):
    labels = [outcome(r) for r in rows]
    # Dead jobs and client-closed jobs say nothing about the letter, so they leave the denominator.
    judged = [l for l in labels if l not in {"pending", "dead", "closed", "withdrawn"}]
    engaged = sum(l in {"engaged", "offered", "hired"} for l in labels)
    connects = sum((num(r.get("connects_cost")) or 0) + (num(r.get("boost_connects")) or 0) for r in rows)
    connects_missing = sum(num(r.get("connects_cost")) is None for r in rows)
    return {
        "n": len(rows),
        "judged": len(judged),
        "pending": labels.count("pending"),
        "dead": labels.count("dead"),
        "closed": labels.count("closed"),
        "passed_over": labels.count("passed_over"),
        "connects_missing": connects_missing,
        "engaged": engaged,
        "hired": labels.count("hired"),
        "engaged_rate": round(engaged / len(judged), 3) if judged else None,
        "connects": int(connects),
        "connects_per_engaged": round(connects / engaged, 1) if engaged else None,
        "confidence": "act" if len(judged) >= MIN_BUCKET else "observe",
    }


def group(rows, key, total_judged):
    buckets = {}
    for row in rows:
        buckets.setdefault(key(row), []).append(row)
    out = {k: stats(v) for k, v in sorted(buckets.items())}
    # A bucket can only be actionable once the whole dataset is, otherwise "[act]" contradicts
    # weights_change_allowed=False on the same report.
    if total_judged < MIN_TOTAL:
        for s in out.values():
            s["confidence"] = "observe"
    return out


def cmd_summary(as_json):
    rows = load()
    overall = stats(rows)
    total = overall["judged"]
    if total < MIN_TOTAL:
        overall["confidence"] = "observe"
    report = {
        "generated_utc": now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "overall": overall,
        "weights_change_allowed": total >= MIN_TOTAL,
        "by_cohort": group(rows, lambda r: r.get("cohort") or "unknown", total),
        "by_wedge_type": group(rows, lambda r: r.get("wedge_type") or "none", total),
        "by_score_band": group(rows, score_band, total),
        "by_rate_band": group(rows, rate_band, total),
        "by_boosted": group(rows, lambda r: r.get("boosted") or "unknown", total),
        "by_rule_version": group(rows, lambda r: r.get("rule_version") or "unknown", total),
        "rows": [{"proposal_id": r["proposal_id"], "title": r["title"][:50], "outcome": outcome(r)} for r in rows],
    }
    if as_json:
        print(json.dumps(report, indent=2))
        return

    def line(name, s):
        rate = f"{s['engaged_rate']:.0%}" if s["engaged_rate"] is not None else "n/a"
        cpe = s["connects_per_engaged"] if s["connects_per_engaged"] is not None else "n/a"
        missing = f" ({s['connects_missing']} unrecorded)" if s["connects_missing"] else ""
        return (f"  {name:<22} n={s['n']:<3} judged={s['judged']:<3} engaged={s['engaged']:<2} "
                f"passed_over={s['passed_over']:<2} dead={s['dead']:<2} rate={rate:<5} "
                f"connects={s['connects']}{missing} per-engaged={cpe} [{s['confidence']}]")

    print(f"OUTCOMES  {report['generated_utc']}")
    print(line("overall", overall))
    print(f"  weight changes allowed: {report['weights_change_allowed']} "
          f"(needs {MIN_TOTAL} judged, have {overall['judged']})")
    for title, key in [("COHORT", "by_cohort"), ("WEDGE TYPE", "by_wedge_type"),
                       ("SCOUT SCORE", "by_score_band"), ("RATE", "by_rate_band"),
                       ("BOOSTED", "by_boosted"), ("RULE VERSION", "by_rule_version")]:
        print(title)
        for name, s in report[key].items():
            print(line(name, s))
    print("ROWS")
    for r in report["rows"]:
        print(f"  {r['proposal_id']}  {r['outcome']:<11} {r['title']}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    command = sys.argv[1]
    if command == "add" and len(sys.argv) == 3:
        cmd_add(sys.argv[2])
    elif command == "update" and len(sys.argv) == 4:
        cmd_update(sys.argv[2], sys.argv[3])
    elif command == "due":
        cmd_due()
    elif command == "summary":
        cmd_summary("--json" in sys.argv)
    else:
        sys.exit(__doc__)
