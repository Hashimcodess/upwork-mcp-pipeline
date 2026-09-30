#!/usr/bin/env python3
"""Job ledger for the dummy-portfolio-creation skill.  Stdlib only.

Fully independent: reads and writes only its own data/job-ledger.jsonl.
Never touches any other skill's files.

Why it exists: the Upwork API only returns currently open jobs, and search reaches back
about three weeks. Every validation run appends what it saw to this ledger, so the evidence
window grows toward the 3-4 months the skill wants. Counts pulled from the API for older
weeks are LOWER BOUNDS (filled and expired jobs drop out); the ledger is the trusted record.

All "now" maths anchor on the newest published date in the ledger (or --anchor), never on the
machine clock, which runs about 12 hours behind on this machine.

Commands
  add    --file records.json [--source search|smart|manual] [--now ISO]
  stats  --terms "a,b,c" [--must "x,y"] [--exclude "z"] [--days 120] [--anchor ISO]
  span
Global: --ledger PATH (default data/job-ledger.jsonl, used for tests)
"""
import argparse
import json
import math
import os
import statistics
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_LEDGER = os.path.normpath(os.path.join(HERE, "..", "data", "job-ledger.jsonl"))


def parse_ts(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).astimezone(timezone.utc)
    except (ValueError, TypeError):
        return None


def iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ") if dt else None


def load(path):
    records = {}
    if not os.path.exists(path):
        return records
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if rec.get("id"):
                records[str(rec["id"])] = rec
    return records


def save(path, records):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    ordered = sorted(records.values(), key=lambda r: r.get("published") or "", reverse=True)
    with open(path, "w", encoding="utf-8") as fh:
        for rec in ordered:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")


def to_num(value):
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return float(value)
    cleaned = "".join(ch for ch in str(value) if ch.isdigit() or ch == ".")
    try:
        return float(cleaned) if cleaned else None
    except ValueError:
        return None


def normalise(raw, source, seen):
    return {
        "id": str(raw.get("id") or raw.get("job_id") or "").replace("~02", "").replace("~", ""),
        "title": (raw.get("title") or "").strip(),
        "published": iso(parse_ts(raw.get("published") or raw.get("published_date") or raw.get("created_date"))),
        "type": raw.get("type") or raw.get("job_type"),
        "budget": raw.get("budget"),
        "proposals": to_num(raw.get("proposals") if raw.get("proposals") is not None else raw.get("proposal_count")),
        "proposals_tier": raw.get("proposals_tier"),
        "skills": raw.get("skills") or [],
        "snippet": (raw.get("snippet") or raw.get("description_snippet") or "")[:400],
        "client_key": raw.get("client_key") or "",
        "client_spent": to_num(raw.get("client_spent")),
        "source": source,
        "first_seen": seen,
        "last_seen": seen,
    }


def cmd_add(args):
    records = load(args.ledger)
    with open(args.file, "r", encoding="utf-8") as fh:
        batch = json.load(fh)
    if isinstance(batch, dict):
        batch = batch.get("jobs") or batch.get("records") or []
    published = [parse_ts(r.get("published") or r.get("published_date") or r.get("created_date")) for r in batch]
    published = [p for p in published if p]
    seen = args.now or (iso(max(published)) if published else iso(datetime.now(timezone.utc)))
    added = updated = skipped = 0
    for raw in batch:
        rec = normalise(raw, args.source, seen)
        if not rec["id"] or not rec["published"]:
            skipped += 1
            continue
        old = records.get(rec["id"])
        if old is None:
            records[rec["id"]] = rec
            added += 1
            continue
        old["last_seen"] = seen
        for key in ("title", "budget", "proposals_tier", "skills", "snippet", "client_key", "client_spent", "type"):
            if rec.get(key) not in (None, "", []):
                old[key] = rec[key]
        if rec["proposals"] is not None:
            old["proposals"] = rec["proposals"]
            old["proposals_max"] = max(rec["proposals"], old.get("proposals_max") or 0)
        updated += 1
    save(args.ledger, records)
    print(json.dumps({"added": added, "updated": updated, "skipped_no_id_or_date": skipped,
                      "ledger_total": len(records)}))


def ledger_anchor(records, override):
    if override:
        dt = parse_ts(override)
        if dt:
            return dt
    stamps = [parse_ts(r.get("published")) for r in records.values()]
    stamps = [s for s in stamps if s]
    return max(stamps) if stamps else datetime.now(timezone.utc)


def match(rec, terms, must, exclude):
    text = " ".join([rec.get("title", ""), rec.get("snippet", ""), " ".join(rec.get("skills") or [])]).lower()
    if exclude and any(x in text for x in exclude):
        return False
    if must and not all(m in text for m in must):
        return False
    return any(t in text for t in terms) if terms else bool(must)


def split(csv):
    return [t.strip().lower() for t in (csv or "").split(",") if t.strip()]


def cmd_stats(args):
    records = load(args.ledger)
    if not records:
        print(json.dumps({"error": "ledger is empty", "hint": "run add first"}))
        return
    anchor = ledger_anchor(records, args.anchor)
    stamps = [parse_ts(r.get("published")) for r in records.values()]
    stamps = [s for s in stamps if s]
    oldest, newest = min(stamps), max(stamps)
    span_days = max(1, math.ceil((newest - oldest).total_seconds() / 86400))
    window = min(args.days, span_days)
    cutoff = anchor - timedelta(days=window)

    terms, must, exclude = split(args.terms), split(args.must), split(args.exclude)
    hits = []
    for rec in records.values():
        pub = parse_ts(rec.get("published"))
        if pub and pub >= cutoff and match(rec, terms, must, exclude):
            hits.append((pub, rec))
    hits.sort(key=lambda x: x[0], reverse=True)

    by_client = defaultdict(list)
    for pub, rec in hits:
        by_client[rec.get("client_key") or ("job-" + rec["id"])].append((pub, rec))
    unique_clients = len(by_client)
    repeat_posters = sorted(
        ({"client": k, "posts": len(v)} for k, v in by_client.items() if len(v) > 1),
        key=lambda d: -d["posts"])[:8]

    weeks = max(1, math.ceil(window / 7))
    weekly = [0] * weeks
    weekly_clients = [set() for _ in range(weeks)]
    for pub, rec in hits:
        idx = min(weeks - 1, int((anchor - pub).total_seconds() // (7 * 86400)))
        weekly[idx] += 1
        weekly_clients[idx].add(rec.get("client_key") or ("job-" + rec["id"]))
    weekly_out = [{"weeks_ago": i, "posts": weekly[i], "unique_clients": len(weekly_clients[i])}
                  for i in range(weeks)]

    trend = "not scored (window under 28 days)"
    if window >= 28:
        mid = anchor - timedelta(days=window / 2)
        older = {(r.get("client_key") or "job-" + r["id"]) for p, r in hits if p < mid}
        newer = {(r.get("client_key") or "job-" + r["id"]) for p, r in hits if p >= mid}
        if not older and newer:
            trend = "up (nothing in the older half)"
        elif older and not newer:
            trend = "down (nothing in the newer half)"
        elif older:
            ratio = len(newer) / len(older)
            trend = "up" if ratio >= 1.3 else "down" if ratio <= 0.7 else "flat"
            trend += " (newer half %d clients vs older half %d)" % (len(newer), len(older))

    props = [r["proposals"] for _, r in hits if r.get("proposals") is not None]
    tiers = Counter(r.get("proposals_tier") for _, r in hits if r.get("proposals") is None and r.get("proposals_tier"))
    spends = []
    for entries in by_client.values():
        s = [r["client_spent"] for _, r in entries if r.get("client_spent") is not None]
        if s:
            spends.append(max(s))
    types = Counter((r.get("type") or "unknown") for _, r in hits)

    if window >= 84 and len(hits) >= 10:
        confidence = "HIGH"
    elif window >= 28 and len(hits) >= 5:
        confidence = "MEDIUM"
    else:
        confidence = "LOW"

    print(json.dumps({
        "anchor": iso(anchor),
        "ledger": {"records": len(records), "oldest": iso(oldest), "newest": iso(newest), "span_days": span_days},
        "window_days_used": window,
        "requested_days": args.days,
        "confidence": confidence,
        "matches": len(hits),
        "unique_clients": unique_clients,
        "repeat_posters": repeat_posters,
        "weekly": weekly_out,
        "trend": trend,
        "proposals": {"numeric_n": len(props),
                      "median": statistics.median(props) if props else None,
                      "p75": sorted(props)[int(0.75 * (len(props) - 1))] if props else None,
                      "tiers_only": dict(tiers)},
        "client_spend": {"clients_with_spend": len(spends),
                         "median": statistics.median(spends) if spends else None,
                         "share_5k_plus": round(sum(1 for s in spends if s >= 5000) / len(spends), 2) if spends else None},
        "job_types": dict(types),
        "titles": [{"published": iso(p)[:10], "title": r["title"], "proposals": r.get("proposals")}
                   for p, r in hits[:12]],
    }, indent=2))


def cmd_span(args):
    records = load(args.ledger)
    if not records:
        print(json.dumps({"records": 0}))
        return
    stamps = [parse_ts(r.get("published")) for r in records.values()]
    stamps = [s for s in stamps if s]
    oldest, newest = min(stamps), max(stamps)
    per_month = Counter(s.strftime("%Y-%m") for s in stamps)
    print(json.dumps({
        "records": len(records),
        "oldest": iso(oldest),
        "newest": iso(newest),
        "span_days": math.ceil((newest - oldest).total_seconds() / 86400),
        "by_source": dict(Counter(r.get("source") for r in records.values())),
        "by_month": dict(sorted(per_month.items())),
    }, indent=2))


def main():
    parser = argparse.ArgumentParser(description="dummy-portfolio-creation job ledger")
    parser.add_argument("--ledger", default=DEFAULT_LEDGER)
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_add = sub.add_parser("add")
    p_add.add_argument("--file", required=True)
    p_add.add_argument("--source", default="search")
    p_add.add_argument("--now", default=None)
    p_stats = sub.add_parser("stats")
    p_stats.add_argument("--terms", default="")
    p_stats.add_argument("--must", default="")
    p_stats.add_argument("--exclude", default="")
    p_stats.add_argument("--days", type=int, default=120)
    p_stats.add_argument("--anchor", default=None)
    sub.add_parser("span")
    args = parser.parse_args()
    {"add": cmd_add, "stats": cmd_stats, "span": cmd_span}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
