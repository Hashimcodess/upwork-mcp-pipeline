# Upwork MCP Pipeline

Claude Code skills that run Danish Ashraf's Upwork job pipeline end to end through the Upwork MCP
server: scan, score, write, validate, submit, then learn from what happened.

Hashim picks the job. Everything after the pick is automated, including the submit.

## Flow

```
job-scout ──► Hashim picks ──► cover-letter ──► proposal-validator ──► submit
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
