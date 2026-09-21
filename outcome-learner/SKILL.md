---
name: outcome-learner
description: >
  Learns from what actually got replies. Syncs every Upwork proposal's status daily, keeps each one
  tagged with scout score, angle (wedge) type, rate, match % and Connects cost, writes honest
  observations under small samples, and only once 30+ proposals are judged makes bounded,
  confidence-gated changes to the scout's weights and angle preference. Owns the outcome data and
  the learned weights. Triggered by job-scout, called by proposal-validator at submit.
model: sonnet
disable-model-invocation: false
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, mcp__upwork__upwork__list_freelancer_proposals
---

# outcome-learner — the results side of a self-evolving pipeline

**Account:** `org_uid` = `1328310880177278977`.

The rest of the pipeline gets better at **not making mistakes**. This skill makes it better at
**winning**, and it is the only part allowed to change scoring from results. One owner, so the
scout, validator and improver can never tune the same numbers in different directions.

## Where it sits

```
job-scout ── Step 0 ──► outcome-learner SYNC (if due) ──► LEARN (once a day)
    │                           │
    │ reads learned-weights ◄───┘ (only outcome-learner writes it, only when guards pass)
    ▼
Hashim picks ──► cover-letter (reads wedge_preference) ──► proposal-validator ──► Hashim approves
                                                               │ 6g
                                                               ▼
                                              outcome-learner ADD (row at submit)
pipeline-improver Step 1b ── reads observations.md (never edits weights)
performance-evaluator ────── reads summary for the ledger
```

Scans are the one thing that reliably runs, so the scout carries this skill. No separate
scheduler is needed for the loop to keep turning.

## Files

| File | Role |
|---|---|
| `data/outcomes.csv` | One row per proposal: decisions + outcome. The dataset |
| `data/state.json` | Last sync, last learn, last apply. Gates the daily cadence |
| `scripts/outcomes.py` | **All arithmetic and all weight changes.** Never compute a rate or edit weights by hand |
| `references/observations.md` | Dated record of what the data said on each learning pass |
| `references/calibration-log.md` | Every applied change with its evidence. Empty until guards pass |
| `../job-scout/references/learned-weights.json` | Scout component weights, wedge points, wedge preference. Baseline kept for bounds |

Paths below are relative to `Danish/.claude/skills`.

---

## Step A — ADD (called by proposal-validator 6g at submit)

```
python outcome-learner/scripts/outcomes.py add '<json>'
```

Every row must carry the five tags learning needs: **`scout_score`, `match_pct`, `wedge_type`,
`bid`, `connects_cost`**, plus `comp_*` component fractions (points ÷ weight, 0-1) when the scout
scored the job, and `rule_version` = `git rev-parse --short HEAD`. The script warns on missing tags.
A job Hashim picked without a scout card gets blank scout fields; blank beats guessed.

`wedge_type` must be one of: `impossible_spec`, `misdiagnosis`, `unstated_failure`, `wrong_tool`,
`buried_real_project`, `scope_trap`, `none`. Take it from `wedge.md`. A letter with no wedge is
`none`, never promoted to a type it does not have.

## Step B — SYNC (daily, triggered by job-scout Step 0)

```
python outcome-learner/scripts/outcomes.py status     # {"sync_due": ..., "learn_due": ...}
python outcome-learner/scripts/outcomes.py due        # proposal ids to refresh
```

For each id: `list_freelancer_proposals action=get params={id:"<id>"}`, then
`outcomes.py update <id> '<json>'`:

| Field | Source |
|---|---|
| `status` | `vendorProposal.status.status`, lowercased. **Per proposal.** The `list` status filter is unreliable |
| `client_messaged` | `yes` if the response has `room_id`, else `no`. The only per-proposal engagement signal the API has |
| `field_total/opened/shortlisted/messaged` | `insights.proposals_total / proposals_opened / shortlisted / messaged`. Job-level context only |

⚠ **Never write "not us" against an OPEN or SHORTLIST number** (added 2026-09-16, after four
ledger notes had to be rewritten). The distinction is not pedantic — it decides whether a loss
gets blamed on the letter:

- `proposals_opened` / `shortlisted` are **job-level totals only.** Upwork exposes no per-proposal
  view flag anywhere. "Client opened 17 of 54 and not ours" is unknowable, and writing it teaches
  the pipeline that the letter failed when the evidence cannot say that.
- `client_messaged` **is** per-proposal (a `room_id` either exists or it does not). So "the client
  messaged 18 people and we were not one of them" is a fact and is fair to record.

Write the job-level number as a job-level number, then state our own outcome separately.
| `last_checked_utc` | now, in UTC |

When `insights_available` is false, leave the field_* values as they were. Never estimate.
Finish with `outcomes.py mark-sync`. If `update` prints `NEW SIGNAL`, job-scout puts that proposal
at the top of the digest.

Outcome labels, strongest first: `hired > offered > engaged > declined > closed > dead >
passed_over > no_response > pending`. **Judged** (counts toward learning) = engaged, offered,
hired, declined, passed_over, no_response. Dead and closed jobs are scout problems and never
count against a letter.

## Step C — LEARN (once a day, when `learn_due`)

```
python outcome-learner/scripts/outcomes.py learn            # always
python outcome-learner/scripts/outcomes.py gaps             # untagged rows to fix
```

The script prints and records: stage, engaged rate with 90% interval, every wedge type against all
other judged letters, whether scout score actually separates engaged from not, whether scout
components do, a version check (newest rules vs the previous version), and every `passed_over`
letter. It appends one dated entry to `observations.md`.

**Then read the passed-over letters yourself**, next to the engaged ones: hook type, wedge type,
length, proof, rate. That qualitative read is allowed at any sample size, but it goes into
`observations.md` labelled `(from N letters, not significant)`. It never changes weights.

## Step D — APPLY (only when the guards pass)

```
python outcome-learner/scripts/outcomes.py learn --apply
```

The guards are code, not judgment. `--apply` refuses on its own when they are not met.

| Stage | Judged | What is allowed |
|---|---|---|
| **observe** | < 30 | **Nothing is changed.** Observations only. This is Hashim's rule: at ~1 proposal a day, 30-50 results are needed before scoring changes mean anything |
| **calibrate** | 30-49 | **Strong** changes only: a wedge type whose 90% interval does not overlap the rest's (±3 points), or a component whose engaged-vs-other mean differs by ≥0.20 (±2 points). Both sides need ≥8 judged |
| **confident** | 50+ | Strong changes, plus **lean** changes of ±1 when a bucket differs by ≥15 points (wedge) or ≥0.10 (component), both sides ≥8 |

Always, whatever the stage:
- Every value stays within **50%-150% of baseline**. Component weights renormalise to 100
- At most **one apply per 7 days**, so each change gets its own rule-version group to be judged by
- `wedge_preference` is re-derived from wedge points after every apply

**After an apply:** commit with the printed evidence in the message. This produces a new
`rule_version`, and every later submission is attributed to it.

**Revert rule.** The version check compares the newest rule version against the previous one once
both have ≥15 judged. `REVERT CANDIDATE` (intervals separate, newest worse): `git revert` the
calibration commit, log it in `calibration-log.md`, tell Hashim. `WATCH`: note it in observations,
change nothing.

## Step E — Persist

```
cd Danish/.claude/skills
git add outcome-learner job-scout/references/learned-weights.json
git commit -m "outcomes: daily sync (<judged> judged, stage <stage>)"      # or
git commit -m "calibration: <changes> — evidence: <bucket numbers>"
```
Push follows the once-every-24-hours rule in `pipeline-improver` Step 4d. Never push on every sync.

A sync with no status changes and no new observation makes no commit.

## Report

```
OUTCOMES  stage observe · judged 9 of 30 needed · engaged 2 (22%, ci90 7-48%)
NEW       none since last sync
WEDGE     impossible_spec 1/1 · misdiagnosis 1/3 · none 0/3 · (all n<8, observe)
SCOUT     engaged mean score 81 (n=1) vs 72 (n=2) — not enough scored rows
VERSION   only one rule version so far
PASSED    5 letters — house detection, wall replacement, GIS, generative video, sales agent
APPLIED   nothing (stage=observe)
```

Notify only on a `NEW SIGNAL`, an applied calibration, or a `REVERT CANDIDATE`.

## Never

- Change `learned-weights.json`, `scoring-rubric.md` weights or wedge points by hand from results
- Lower the guards to make a change happen sooner
- Count a dead or closed job against a letter
- Fill a missing tag with a guess to make a bucket bigger
- Present job-level insights (opened, shortlisted) as if they were about Danish's proposal
