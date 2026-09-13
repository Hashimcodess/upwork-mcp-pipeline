---
name: performance-evaluator
description: >
  Track Danish's Upwork funnel from the CLI: proposals sent, client open rate, shortlist rate,
  message rate, interviews, hires, invitations, Connects burn and earnings. Benchmarks Danish
  against the competing field on every job. Appends to a ledger so trends are visible over time.
model: sonnet
disable-model-invocation: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, PushNotification, mcp__upwork__upwork__list_freelancer_proposals, mcp__upwork__upwork__get_profile, mcp__upwork__upwork__get_freelancer_dashboard, mcp__upwork__upwork__list_contracts, mcp__upwork__upwork__get_freelancer_financials, mcp__upwork__upwork__find_jobs
---

# performance-evaluator — the accountability ledger

Answers one question honestly: **is the pipeline working, and if not, where is it leaking?**

**Account:** `org_uid` = `1328310880177278977`.

The point is to run Upwork from the CLI so Hashim rarely opens the UI. Where the API cannot supply
a number, say so plainly rather than guessing — a fabricated metric is worse than a missing one.

---

## ⚠️ What is actually measurable — read this before building any funnel
**(Corrected 2026-09-07. The original funnel assumed a measurement that does not exist.)**

`insights` returns **job-level** counts, not per-proposal status. `proposals_opened: 31` means the
client opened 31 proposals in that field. **It does not say whether Danish's was one of them.**
Same for `shortlisted` and `messaged`. There is no API field anywhere that reports whether a
specific proposal was read.

So there are two separate things to track, and conflating them produces a fake funnel:

### Track A — Danish's own progression (real, per-proposal)
From proposal `status`: **Accepted/Submitted → Offered → Hired**. Also `Declined`, `Withdrawn`.
This is the only individually-attributable outcome data. It is coarse but it is true.

### Track B — client activity level (real, job-level)
From `insights`: how hard is this client working the pile?

| Pattern | Read |
|---|---|
| opened ≈ total, high shortlisted, high messaged | **Hot.** Client is actively hiring right now |
| opened high, shortlisted 0 | Reading but unconvinced by the whole field |
| opened 0 after 24h+ | **Cold or dead.** Says nothing about any proposal's quality |
| opened 0 under ~6h | Too early. Not a signal |

**Never present Track B as if it were Track A.** "31 of 32 opened" is a statement about the
client's behaviour, not about Danish's letter.

### Track C — field benchmarking (real, and the most actionable)
`applicants_avg_earnings`, `applicants_avg_jss`, `applicants_avg_completed_jobs`,
`applicants_avg_years_on_upwork`, `applicants_top_skills`. Compare Danish against each. Where he
sits **below** the field on a profile-level signal, that is a structural gap no cover letter can
close — route it to `portfolio-profile-upgrade`.

---

## The funnel, as far as it goes

```
SUBMITTED  ->  OFFERED  ->  HIRED        (Track A: real, per-proposal)
     ^
     |  client activity + field strength (Tracks B and C: context, not attribution)
```

- Low **submitted → offered** across many proposals with *hot* clients: the letter or the profile.
- Low submitted → offered where clients are *cold*: targeting. You are picking dead jobs.
- **Offered → hired**: negotiation, rate, availability. Human problem, surface to Hashim.

Separating "cold client" from "warm client who passed on us" is the whole diagnostic value, and
Track B is what makes it possible.

---

## Step 0 — Outcome sync (daily, run FIRST) (added 2026-09-14)

The ledger below is prose. Prose cannot be recalibrated from. `data/outcomes.csv` is the
structured record the whole self-improving loop runs on: one row per proposal, the decisions that
produced it, and what happened. `scripts/outcomes.py` does every calculation; never compute a rate
by hand.

```
python performance-evaluator/scripts/outcomes.py due
```

For each proposal id it prints:
```
list_freelancer_proposals action=get params={id:"<proposal_id>"}
```
and write back with `outcomes.py update <id> '<json>'`:

| Field | From |
|---|---|
| `status` | `vendorProposal.status.status`, lowercased. **Read it per proposal.** The `list` status filter is unreliable (a `Declined` filter returned `Accepted` rows, 2026-09-14) |
| `client_messaged` | `yes` if the response carries `room_id`, else `no`. **This is the only per-proposal engagement signal in the API.** A room exists only when the client started a conversation |
| `field_total` / `field_opened` / `field_shortlisted` / `field_messaged` | `insights.proposals_total` / `proposals_opened` / `shortlisted` / `messaged`. Job-level context, used to separate dead jobs from live losses |
| `last_checked_utc` | now |

Leave a field blank when the API does not give it. Never estimate.

The script derives the outcome: `hired > offered > engaged (room exists) > declined > closed >
dead (0 opened after 24h) > no_response (7d+) > pending`. Dead and closed jobs leave the
denominator, because they say nothing about the letter.

**The strongest learning rows are live losses:** client opened most of the field and messaged
others, but not Danish. Those are the letters that were read and lost. Mark them in `notes`.

Then run `outcomes.py summary` and paste it at the top of the ledger entry. Commit
`data/outcomes.csv` in the skills repo with message `outcomes: daily sync`.

---

## Step 1 — Pull the data

```
get_freelancer_dashboard action=check
list_freelancer_proposals action=list   params={status:"Accepted",  limit:10}   # submitted
list_freelancer_proposals action=list   params={status:"Offered",   limit:10}
list_freelancer_proposals action=list   params={status:"Hired",     limit:10}
list_freelancer_proposals action=list   params={status:"Declined",  limit:10}
list_freelancer_proposals action=invitations params={status:"pending"}
get_profile action=connects_balance     params={limit:10}
```

Page with the cursor while `hasNextPage` is true. `totalCount` on the Accepted list is the
lifetime submitted count.

**Then, per recent proposal, pull insights — this is the core of the skill:**

```
list_freelancer_proposals action=get params={proposal_id:"<id>"}
```

The `insights` block gives, per job:

| Field | Meaning |
|---|---|
| `proposals_total` | Size of the field |
| `proposals_opened` / `proposals_unopened` | How many the client actually read |
| `shortlisted` | How many made the shortlist |
| `messaged` | How many the client contacted |
| `applicants_avg_earnings` | Lifetime earnings of the competing field |
| `applicants_avg_jss` | Their average Job Success Score |
| `applicants_avg_completed_jobs` | Their average completed contracts |
| `applicants_avg_years_on_upwork` | Their average tenure |
| `applicants_top_skills` | What the field is selling |

**`insights` refresh hourly and lag a freshly submitted proposal.** A zero on a proposal submitted
20 minutes ago means "not computed yet", not "ignored". Say which it is.

When `insights_available` is false, relay `insights_note` verbatim. Never say a job has no other
applicants, and never estimate the numbers.

---

## Step 2 — Compute

**Rates.** Only over proposals old enough to have refreshed insights (24h+):

```
open rate       = sum(opened_by_client)   / proposals_with_insights
shortlist rate  = sum(shortlisted_us)     / proposals_with_insights
message rate    = messaged_count          / proposals_sent
offer rate      = Offered count           / proposals_sent
hire rate       = Hired count             / proposals_sent
connects/hire   = total Connects spent    / hires
cost per open   = total Connects spent    / opens
```

**Client-side vs Danish-side.** Critical distinction. If `proposals_opened` is 0 out of 44, the
client has not read *anyone*. That is a dead job, not a bad letter. Separate:
- **Dead jobs** — `proposals_opened` = 0 across the whole field
- **Live jobs where Danish was not opened** — client opened others, not him. That IS a signal.
- **Opened but not shortlisted** — the letter was read and lost. The strongest signal available.

Report the second and third categories as the real denominator. Averaging dead jobs into the open
rate makes the letter look worse than it is and points the fix at the wrong place.

**Field benchmarking.** For each job compare Danish against `applicants_avg_*`. He is Top Rated
Plus, so where he is *below* the field average on earnings or JSS, that job was a stretch and the
targeting rule should learn from it. Where he is well above and still not opened, the problem is
rank or timing, not credentials.

**Skills gap.** Aggregate `applicants_top_skills` across recent jobs. Skills that keep appearing
in the competing field but are missing from Danish's 20 are a concrete profile action — hand them
to `portfolio-profile-upgrade`.

---

## Step 3 — Ledger

Append one row per run to `Danish/performance/ledger.md`. Never rewrite history; the trend is the
product.

```
## 2026-09-07

FUNNEL (lifetime)     sent 14 · offered 0 · hired 0
FUNNEL (last 7d)      sent 5 · opened 1/4 live · shortlisted 0 · messaged 0

RATES (insight-eligible proposals only, n=4)
  open       25%   (1 of 4 live jobs; 1 job dead-on-arrival, excluded)
  shortlist   0%
  message     0%

CONNECTS  spent 72 this week · balance 459 · 0 hires · cost/hire n/a

FIELD vs DANISH
  job 2096348 (drone)  field avg $141k / 0.994 JSS / 28 jobs / 5.5y — 0 of 44 opened, DEAD JOB
  job 2096699 (legal)  field avg ... 

SKILLS SEEN IN FIELD, MISSING FROM PROFILE
  Full-Stack Development (4 applicants) · Data Analytics (2)

LEAK DIAGNOSIS  Too early to call. n=4 insight-eligible, 1 dead job.
                Need 10+ before any rate is meaningful.
```

**Small-n honesty.** Below ~10 insight-eligible proposals, do not report a rate as if it means
something. Say `n too small` and give the raw counts. A 0% hire rate on 5 proposals is noise.

---

## Step 4 — Diagnose and recommend

One diagnosis, the highest-leverage leak only. Not a list of everything imperfect.

| Symptom | Likely cause | Action |
|---|---|---|
| Low open rate on **live** jobs | Rank. Applying late, or crowded jobs, or unboosted | Tighten `job-scout` staleness filter; consider boost on high-value jobs |
| Whole fields unopened | Dead jobs | Add a `proposals_opened == 0` check on jobs older than 24h to the scout hard filters |
| Opened, never shortlisted | The letter | Route to `pipeline-improver`. The wedge is not landing |
| Shortlisted, never messaged | Rate or proof | Rate is above the field, or the profile does not back the letter. Route to `portfolio-profile-upgrade` |
| Messaged, never hired | Negotiation or capacity | Human problem. Surface to Hashim |
| High Connects burn, no opens | Targeting | Raise the scout score threshold |

---

## What the API cannot give — say this every time it comes up

**Profile views, impressions, and clicks are NOT exposed by the Upwork MCP.** There is no endpoint
for them in `get_profile`, `get_freelancer_dashboard`, or anywhere else in the server. They live
on Upwork's own profile-insights page in the web UI.

Do not estimate them. Do not proxy them with something else and call them impressions. When
Hashim asks, tell him this is the one number that still needs the UI, and offer to record it in
the ledger if he reads it off and pastes it — a `MANUAL` row keeps the trend intact:

```
MANUAL (from UI, 2026-09-07)  profile views 34 · impressions 1,204 · clicks 61
```

**What IS available and covers most of it:** invitations received (`action=invitations`), message
rooms and activity (`get_messages`), proposal opens/shortlists/messages (the insights block),
Connects flow, earnings, and contract status. That is the whole funnel except top-of-funnel
profile impressions.

---

## Cadence

Run daily. Weekly, add a 7-day trend block comparing to the prior week.

Notify only when something is actionable:
```
PushNotification status="proactive"
message="Upwork week: 5 sent, 1 of 4 live jobs opened, 0 shortlisted. 1 dead job excluded. Leak is at open stage - applying too late."
```

Do not notify a routine no-change day. A daily "nothing happened" push trains Hashim to ignore
the channel.
