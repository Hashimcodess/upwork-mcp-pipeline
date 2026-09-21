# Upwork MCP Pipeline

Claude Code skills that run Danish Ashraf's Upwork job pipeline end to end through the Upwork MCP
server: scan, score, write, validate, submit, then learn from what happened.

Hashim picks the job. Letter writing and validation are automated. **Nothing is submitted until
Hashim has reviewed the final cover letter and explicitly approved it** (hard rule, revised
2026-09-21 — was: everything after the pick automated, including the submit).

## Flow

```
job-scout ──► Hashim picks ──► cover-letter ──► proposal-validator ──► Hashim reviews ──► submit
    ▲                                                   │
    │                                                   ▼
    └──────────── pipeline-improver ◄──── performance-evaluator (outcomes)
```

| Skill | Role |
|---|---|
| `job-scout` | Scans Upwork feeds, applies hard filters, scores /100, writes a mobile digest |
| `cover-letter` | Finds the wedge (one falsifiable technical claim), researches it, writes letter + screening answers |
| `proposal-validator` | Gate 0 "will this win", claim verification, voice, compliance, then liveness check and submit |
| `pipeline-improver` | Runs after every submit. Audits the run, edits the skill files, persists the lesson |
| `performance-evaluator` | Funnel ledger from proposal status and job insights |
| `portfolio-profile-upgrade` | Portfolio pieces and profile keywords from live demand |

## Requirements

- Claude Code with the Upwork MCP server (`https://mcp.upwork.com/mcp`) authenticated
- `org_uid` for the freelancer account (hardcoded in the skills for Danish)
- These skills live at `<profile>/.claude/skills/` so Claude Code loads them for that profile

## How the pipeline evolves

Every change `pipeline-improver` makes to a skill file should land as a commit here, with the
reason in the message. That gives a dated, reversible history of every rule.

Rule of thumb for edits:
- Dated marker on every change: `(added YYYY-MM-DD)` or `(revised YYYY-MM-DD — was X)`
- Never silently delete a rule; supersede it and say why
- Keep files tight. A rule that never fires is load cost with no benefit

## Outcome loop — the `outcome-learner` skill (built 2026-09-14)

The rest of the pipeline learns from **mistakes**. `outcome-learner` learns from **results**, and
it is the only component allowed to change scoring from them.

- `outcome-learner/data/outcomes.csv`: one row per proposal. Decisions (rule version, scout score
  and its six components, match %, wedge type, rate, Connects) and outcome (status, whether the
  client opened a conversation, job-level field activity)
- `outcome-learner/scripts/outcomes.py`: all arithmetic and all weight changes
- `job-scout/references/learned-weights.json`: scout component weights, wedge points, wedge
  preference. Baseline kept for bounds

```
python outcome-learner/scripts/outcomes.py status          # sync / learn due?
python outcome-learner/scripts/outcomes.py learn           # observations, recommendations, version check
python outcome-learner/scripts/outcomes.py learn --apply   # applies only if the guards pass
python outcome-learner/scripts/outcomes.py summary         # breakdowns with 90% intervals
python outcome-learner/scripts/outcomes.py gaps            # rows missing learning tags
```

**Sample-size discipline, enforced in code:**

| Stage | Judged proposals | Allowed |
|---|---|---|
| observe | < 30 | Observations only. Nothing changes |
| calibrate | 30-49 | ±3 wedge points when 90% intervals separate; ±2 component points on a ≥0.20 gap |
| confident | 50+ | Also ±1 lean changes on a ≥15-point / ≥0.10 gap |

Every value stays within 50-150% of baseline, at most one apply per 7 days, every apply is a
commit, and a newer rule version that performs clearly worse than the previous one (15+ judged in
each) is flagged for `git revert`.

Wiring: the validator adds a row at submit, the scout triggers sync and the daily learning pass,
the cover letter reads the learned wedge preference, pipeline-improver reads observations.

## Known limits (verified)

- Client attachments are not returned by `find_jobs get`
- Client review text, profile views and impressions are not exposed
- No portfolio write API for individual freelancers
- Cloud routines cannot reach the Upwork MCP; scheduling is session-scoped `CronCreate`
- Proposal insights counts are job-level, not per-proposal

## Roadmap

1. **Outcome loop.** Daily status pull per proposal (opened, messaged, interview, hired, archived),
   tagged with scout score, wedge type, rate and Connects cost. Recalibrate from outcomes, not only
   from caught mistakes. Needs 30-50 outcomes before weight changes mean anything.
2. **Session-independent scheduling.** Test Windows Task Scheduler running Claude Code headless
   with the local Upwork MCP.
3. **Rule budget.** Adding a rule requires merging or pruning one; prune rules that have not fired
   in 30 days.
4. **Connects ROI.** Track Connects spent per reply and feed it into scout scoring.
