---
name: job-scout
description: >
  Scan Upwork for jobs matching Danish's profile (computer vision, AI/ML, drones,
  embedded systems), score them against hard filters and ranking signals, pull full
  client metrics for survivors, and deliver a mobile-scannable ranked digest plus a
  push notification. Use for routine hourly scouting or an on-demand scan.
model: sonnet
disable-model-invocation: false
allowed-tools: Read, Write, Glob, Grep, PushNotification, mcp__upwork__upwork__find_jobs, mcp__upwork__upwork__get_freelancer_dashboard, mcp__upwork__upwork__list_freelancer_proposals
---

# job-scout — Upwork scouting + validation for Danish

Find the few jobs worth Danish's time, prove they are worth it with real numbers, and put
the decision in front of Hashim in a form he can read on a phone in 30 seconds.

**Account:** `org_uid` = `1328310880177278977` (Danish Ashraf). Pass it directly to every call.

**Your output is a decision aid, not a decision.** Hashim picks. Never apply, never draft a
cover letter here. Rank, evidence, hand over.

---

## Step 0 — Pre-checks (always, never skip)

```
get_freelancer_dashboard action=check
list_freelancer_proposals action=invitations  params={status: "pending"}
```

From the dashboard capture: Connects balance, any pending invitations, any offers, and new
client messages. If there are **invitations or offers**, surface those at the very top of the
digest — an invitation beats any marketplace job and costs no Connects.

**Outcome loop** (added 2026-09-14, revised same day — moved to its own skill). Scans are the one
thing that reliably runs, so they carry the learning loop:
```
python outcome-learner/scripts/outcomes.py status
```
- `sync_due: true` → run `outcome-learner` Step B before scanning (a handful of `get` calls)
- `learn_due: true` → run `outcome-learner` Step C after the sync (once a day)

Any proposal that prints `NEW SIGNAL` goes at the top of the digest next to invitations. Add one
line to the digest footer: `LEARNING  stage <stage> · judged <n> of 30`.

---

## Step 1 — Scan

**Scope: Danish's WHOLE profile and portfolio, not a fixed shortlist of verticals.**
(Revised 2026-09-07 — was four verticals: CV, drones, embedded, ML.)

Before scoring, the relevant context is:
- `Danish/profile/upwork-profiles/main-profile.md` — the live profile Uma matches against,
  including its `## Keywords To Mirror` list and the real Upwork work history
- `Danish/profile/profile-summary.md`
- All **40** files in `Danish/projects/*.md`
- `Danish/CLAUDE.md` `## Primary Domains`

A job is in scope if **anything in that body of work** gives a genuine ≥40% match. The four
domains Hashim named are where he is strongest, not a filter.

Run these in parallel.

**A. Personalized feeds (primary — Upwork's recommender already knows the full profile, so this
is the broadest net available):**
```
find_jobs action=smart_search params={mode: "most_recent", days_posted: 2, limit: 10}
find_jobs action=smart_search params={mode: "best_match", limit: 10}
```

`days_posted: 2` enforces the age cap at the API for the most_recent feed — the only feed that has
a real date filter. **`best_match` ignores date entirely and `action=search` has no date filter at
all**, so everything from those two must be age-checked client-side against `published_date`
before it reaches scoring. That is where the 30-day-old job slipped through on 2026-09-07.

**B. Marketplace recency searches (secondary — catches what the recommender misses). Rotate
through these; run all seven on a full scan, or 4-5 on a light one:**
```
1. "computer vision object detection tracking segmentation image video"
2. "LiDAR point cloud 3D mapping geospatial satellite drone aerial photogrammetry"
3. "embedded edge AI jetson tensorrt firmware microcontroller robotics ROS sensor fusion"
4. "machine learning engineer pytorch tensorflow model training MLOps deployment"
5. "AI agent LLM RAG langchain langgraph multi-agent orchestration automation"
6. "voice AI TTS STT speech conversational agent realtime calls"
7. "generative AI stable diffusion LoRA fine-tuning image video generation"
```
Each with `sort: "recency", limit: 10`.

Also worth a periodic pass when the board is quiet, because real Upwork contracts back all of
these: data annotation / synthetic data platforms, full-stack AI SaaS, healthcare AI/medical
imaging, VR/3D/facial animation, federated learning, AI-Ops and LLM developer tooling.

**Dedupe** across every result set by job `id`.

**Drop immediately, before scoring:**
- `applied: true` or `is_applied: true` — never re-surface
- Anything already in `references/rejected-jobs.md` (read it first)

Useful filters to add when the run is noisy — they cut junk before it reaches scoring:
- `verified_payment_only: true` — removes unverified clients wholesale
- `proposals_max: 20` — early-mover advantage only
- `rate_min: 40` + `job_type: "hourly"` — enforces the floor at the API level

⚠️ **`client_hires_min` structurally biases toward OLD jobs.** Established clients accumulate
postings, so filtering on hire count pulls up their backlog rather than fresh work. Measured
2026-09-07: a `client_hires_min: 10` search returned 9 of 10 results older than 3 days, four of
them over 17 days, two already filled. The filter is still useful, but **always apply the 48-hour
age cap after it, never instead of it.**

---

## Step 2 — Hard filters (auto-discard, no exceptions)

Discard silently. Do not list these in the digest. Do not ask permission.

| Filter | Rule |
|---|---|
| **Rate floor** | Hourly with `hourlyBudgetMax` < 40, or a fixed budget clearly implying sub-$40/hr for the scope. Standing rule: $40/hr floor. Jobs with **no stated budget still pass** — absence is not a low number. |
| **Portfolio match** | Below 40%. The never-force-fit floor from root `CLAUDE.md`. |
| **AGE — 2 DAYS MAX** | **Posted more than 48 hours ago. No exceptions, no overrides.** Hashim's standing instruction, 2026-09-07: never recommend a job older than 2 days. This supersedes the earlier crowded/dormant staleness rules, which were more complex and let a 30-day-old job through. Check `published_date` (fall back to `created_date`) against now. A great match, a weak field, or an excellent client do **not** buy an exception. |
| **Content-mill signal** | Client's work history is Webflow sites / logos / SEO audits / VA gigs *and* the budget is under $200 for engineering work. |
| **Fake budget** | Stated budget is an order of magnitude below the bid spread (e.g. "$100 fixed" with bids averaging $800). Flag-and-drop unless the post itself says the number is a placeholder. |
| **Language/location gate** | Post requires a language Danish does not have, or hard-requires a country he is not in. |


---

## Step 3 — Score the survivors

Score 0-100. Weights are deliberate: match and client quality dominate, because a perfect
proposal to a client who never hires is wasted Connects.

**Weights come from `references/learned-weights.json` → `current`** (added 2026-09-14). The
numbers in the two tables below are the **baseline**. Only `outcome-learner` changes the JSON, and
only after 30+ judged proposals with confidence-gated evidence. Read the JSON at the start of every
scan. If `current` differs from baseline, use `current` and put `weights: learned <updated_utc>` in
the digest footer.

**Record the components on every surfaced card**, so results can be traced back to which part of
the score actually predicted a reply:
```
COMPONENTS match 24/30 · client 18/25 · wedge 15/15 (misdiagnosis) · competition 5/10 · rate 7/10 · post 10/10
```
Save the same line in the scout report. The validator turns these into `comp_*` fractions at
submit.

| Signal | Weight | How to score |
|---|---|---|
| **Portfolio match %** | 30 | Score against `Danish/projects/*.md`. See `references/scoring-rubric.md` for the domain map. Report the honest number. |
| **Client hire record** | 25 | `client_record.jobs_with_hires` and `spend_total` read **together**. $50k spent across 100 hires is a real buyer; $50k across 1 hire is a one-off. Zero hires = cap this at 5/25 regardless of spend. |
| **Winnability (wedge available)** | 15 | See below. This is the difference between a bet and a lottery ticket. |
| **Competition** | 10 | `proposal_count`. <10 = full marks. 10-25 = half. 25-45 = quarter. 45+ = zero. Crowded fields also take a penalty below. |
| **Rate fit** | 10 | Range midpoint vs Danish's $65 standard. At or above = full. $40-65 = partial. Below floor already filtered. |
| **Post quality** | 10 | Detailed spec, named stack, screening questions = full marks. Three vague sentences = low. |

### Winnability — is there a wedge?

Match tells you Danish *can* do the job. Winnability tells you whether he can *prove it in 200
words* better than 40 other applicants. Read `cover-letter/references/winning-patterns.md` for the
full taxonomy. Scan the post for:

| Wedge | Signal in the post | Score |
|---|---|---|
| **Impossible spec** | A stated accuracy/latency/cost target published results say is unreachable | 15 |
| **Misdiagnosis** | Symptom list implying one cause where there are clearly two | 15 |
| **Unstated failure mode** | Something obvious that breaks in month three and they haven't hit yet | 12 |
| **Wrong tool** | They named a stack that will fight them, and invited opinions | 12 |
| **Buried real project** | Five bullets, four routine, one genuinely hard | 10 |
| **Scope trap** | Budget and scope incompatible; saying so is the differentiator | 8 |
| **None found** | Three vague sentences, no stack, no numbers, no contradictions | 0 |

A job scoring 0 here is a credentials contest against 40 people. High match plus zero wedge is
worth flagging explicitly in the card — Hashim should know he is buying a lottery ticket.

**Name the wedge in the card.** One line. That line is what makes the apply/skip call fast.

**Penalties (subtract after scoring):**
- Client rating below 4.0 → **−15** and flag it loudly. That is other freelancers reporting a
  bad experience with this client, not the client being unsuccessful.
- **Payment unverified → −10.** Read this from `verification_status` in the *search* feeds
  (`VERIFIED` / `NOT_VERIFIED`), not from `canClientReceiveContractProposal`.
  ⚠ **`canClientReceiveContractProposal: false` is NOT a verification signal.** Measured
  2026-09-07: it returned `false` for a client with **$1,982,507 spent, 76 hires and
  `verification_status: VERIFIED`**, and for a second VERIFIED client the same run. The old label
  would have docked 10 points from the best client of the scan. Whatever the flag means, it is not
  payment verification — ignore it for scoring.
  When a job never appears in a feed that reports `verification_status`, record verification as
  **unknown** and apply **no penalty** — say so on the card rather than guessing downward.
- `jobActivity.totalHired > 0` → **−25**. Someone is already hired; the seat may be gone.
- `invitesSent` ≥ 5 with 0 hires → **−5**. Client is shopping hard.

### Crowd and quiet-client WARNINGS (revised 2026-09-16 — warnings, never drops)

Hashim, 2026-09-16: *"all I want is to not have very strong gates, after all our end goal is to
convert the clients and generate business from upwork."* These two started the day as hard
filters and were softened the same afternoon. **They lower the score and put a warning on the
card. They never remove a job from the digest and never write it to `rejected-jobs.md`.**

| Warning | Condition | Penalty | Card line |
|---|---|---|---|
| **Crowded** | `proposal_count` 60-100 | **−10** | `⚠ CROWDED  69 proposals — placement matters more than the letter here; a boost may be the difference.` |
| **Very crowded** | `proposal_count` over 100 | **−20** | `⚠ VERY CROWDED  382 proposals — long shot unless boosted.` |
| **Quiet client** | `proposal_count` ≥ 25 **and** `totalInvitedToInterview` == 0 **and** `invitesSent` == 0 | **−10** | `⚠ QUIET CLIENT  35 proposals, nobody invited or interviewed yet. Could just be early.` |

Why they exist: an audit of the first 18 proposals found 120 of 308 Connects in jobs that got
no traction for anyone — four into fields of 104-516 proposals, and four where the client opened
zero proposals out of the whole field. That is worth knowing on the card. It is not a reason to
hide the job, because Hashim's goal is conversions and a crowded job with a great client is
still sometimes the right bet.

Know which signal exists when: `proposals_opened` only appears in the `insights` block **after**
applying, so it can never be a pre-application warning. The quiet-client check uses
`activityStat.jobActivity` from `find_jobs action=get`, which is available before applying.

A quiet client is often just early. Re-check `jobActivity` on the next scan while the job is
inside the 48h window; if invites or interviews have started, the warning and penalty drop off.

**Bands (revised 2026-09-07 — Hashim dropped the floor to 40 to see more options):**
- **80+** — Strong. Lead the digest with it.
- **65-79** — Full card with all metrics. Push notification.
- **Push floor = surfacing floor = 40.** Every band above is pushed, none is digest-only.
- **40-64** — **Surfaced with real detail**, not a throwaway line. Rate, client record, proposal
  count, match %, the wedge if there is one, and the single reason it scored where it did. He is
  deciding from this, so give him enough to decide on. **Push notification** — see Step 6.
- **<40** — Dropped, logged to `rejected-jobs.md` with the reason.

### ⚠️ The floor is 40, and the scoring must be right
**(Hashim, 2026-09-07: "drop the threshold to 40... I want more options... but remember to
accurately score the jobs and don't discard jobs just because of your mismatched job matching.")**

Two separate obligations, and the second is the harder one.

**1. Surface everything at 40+.** Hashim picks the jobs. The scout informs that choice, it does not
pre-empt it. A lower floor is worthless if the number feeding it is wrong.

**2. Score accurately, which means:**
- **Read the FULL post, never the snippet.** The Radar miss (35 scored, 55 true) happened because
  the snippet omitted "or another sensing field" and the sensor-fusion/GNSS pluses.
- **Apply the cross-domain adjacency section** in the rubric before assigning any match below 50.
- **Never let a high score elsewhere shorten the scan.** That is anchoring and it caused the same
  miss.
- **When genuinely unsure between two match figures, use the higher one and say why.** An
  over-surfaced job costs Hashim ten seconds. An under-scored one he never sees at all.

### Match % vs composite score — do not conflate them

The composite can clear 40 while the *match* is below 40%. That is fine for surfacing, but it
changes what a letter could honestly say.

**Always show match % separately on every card.** When match is under 40%, add one line:
`⚠ match <40% — letter would be approach-led, no portfolio project can be honestly cited.`

That is the never-force-fit rule from root `CLAUDE.md`, and it governs the *letter*, not whether
the job reaches Hashim.

**Surface it regardless of score, always, when any of these are true:**
- Rate range tops at or above the $65 standard
- Client is a serious buyer (real spend AND recent hiring activity)
- The post explicitly invites adjacent backgrounds (see the cross-domain section in the rubric)
- Fewer than 10 proposals
- The job is in a domain Danish has shipped in, even if the specific technique differs

**Do not let a high score elsewhere shorten the rest of the scan.** The Radar job was dropped in a
run where a job scoring 84 had already been found. Finding a winner is not a reason to stop
evaluating — that is anchoring, and it is how the 35%-vs-55% miss happened.

---

## Step 4 — Pull full metrics for everything scoring 40+

**40, not 65.** The 40-64 band promises Hashim rate, client record and proposal count so he can
decide from the digest alone. That promise is unkeepable without the per-job `get` call, so the
metrics floor tracks the surfacing floor. It costs extra API calls per scan; that is the price of
the lower floor, not a reason to skip it.

For each, call:
```
find_jobs action=get params={job_id: "<numeric id>"}
```

Extract, verbatim, no estimating:
- `activityStat.jobActivity` → **proposals, invitesSent, totalHired, totalInvitedToInterview, totalOffered**
- `activityStat.applicationsBidStats` → avg / min / max bid. **Always state the basis is unspecified** — on fixed-price jobs these have been seen as both hourly rates and project totals.
- `client_record` → `spend_total`, `jobs_with_hires`, `contracts_total`, `contracts_active`, `feedback_score`, `feedback_count`, `hours_total`
- `client_work_history` → the **last 3 closed contracts**: title, `feedback_score`, start/end dates
- `connects_cost`, `connects_balance`
- `preferred_qualifications` → and whether Danish clears each one
- `contractTerms` → type, rate range or fixed amount, experience level, engagement

### ⚠️ Attachments are invisible to the API (added 2026-09-14)

`find_jobs get` returns the description only, never the files a client attaches. When the post
says "attached scope", "see the brief", "review the attached", the real scope is somewhere the
scout cannot read. Put this on the card:

`⚠ ATTACHMENT not readable via API — scope and budget may be very different. Needs a manual read before a letter.`

Case: Kitchen & Service Analytics, Bahrain (`2099116033081943645`). Listed as $300 fixed with a
three-sentence description. The attached .docx was a 328-camera, two-country enterprise RFP
asking for a 3-year cost of ownership, itemised hardware and acceptance criteria. Hashim read it
and skipped. Scored 53 on a scope that did not exist.

### ⚠️ Client reviews — a real API limit, state it honestly

**The Upwork MCP does not expose review text.** `client_work_history` returns contract titles,
numeric `feedback_score`, and dates — never the words a freelancer wrote. You cannot quote
reviews and you must never invent one.

What to show instead, labelled exactly like this:

```
Last 3 closed (score only, review text not available via API):
  4.85  No-Code Video Platform          Nov 24 - Jul 25
  5.00  60 minute consultation          Nov 24 - Nov 24
  3.00  Virtual Assistant, Support      Jul 26 - Jul 26   <- low
```

Flag any score below 4.0 in that list. A pattern of low scores is the single most useful
client-quality signal actually available.

---

## Step 5 — The digest (mobile-first)

Hashim reads this on a phone, often on a remote session. Optimise for **information per line**.

Rules:
- No preamble. No "Here's what I found." Start with the first job.
- One card per job, scoring 65+. Max 5 cards. If more qualify, keep the top 5.
- Every number is real and pulled from the API. No estimates, no rounding that changes meaning.
- **40-64 jobs get a compact card, not a one-liner.** Max 5. Each one carries rate, client record,
  proposal count, match %, the wedge if there is one, and the single reason it scored low. A job
  that was worth a push is worth enough detail to act on.
- End with the one-line account state.

**Card format — copy this shape exactly:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. [87] Roofline Segmentation Model
$45-70/hr · hourly · 3h old · 26 Connects
https://upwork.com/jobs/~021234...

MATCH 80%  Satellite Imagery Analytics (aerial
detection, ortho-map), Well Log (U-Net trained
from scratch)

FIELD  6 proposals · 0 invites · 0 hired
       0 interviewing · bids avg $52 (basis n/a)

CLIENT $27,399 · 179 hires · 194 contracts
       4.87 from 138 · 73h · payment VERIFIED
       Last 3 closed (scores only, no review text):
         5.00  RAG system build      Jan-Mar 26
         5.00  AI Usage Assistant    Jan-Apr 26
         4.00  Spec Writer           Jan-Jan 26

GATES  90% JSS ✓ · $1k+ earned ✓ · Rising ✓

WEDGE  Wrong tool. They floated SegFormer-B0; thin
       roof lines into a polyline want U-Net skip
       connections. They asked "tell me why."
RISK   $300 fixed is light for label+train+iterate.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

The `WEDGE` line is the most important line on the card. It is the reason to apply. If it reads
`WEDGE  None found — credentials contest vs 40 applicants`, that is a real and useful answer.

Then:

```
BORDERLINE
  [58] AI Voice Receptionist — 49 proposals, range tops at $50
  [52] Wearable Stress PPG — 45% match, signal-processing focus

ACCOUNT  469 Connects · 0 invites · 0 offers · 4 active
```

---

## Step 6 — Notify

```
PushNotification status="proactive"
message="Upwork scan: 2 strong (Roofline 87, Drone CV 81), 3 borderline. Top: $45-70/hr, 6 proposals, client 179 hires."
```

Rules:
- Under 200 characters. Lead with the count and the single best job's headline numbers.
- **Push whenever anything scores 40+** (Hashim, 2026-09-07: "drop the score threshold to 40+ and
  it push notification"). The push floor and the surfacing floor are now the same number — if a job
  is good enough to reach the digest, it is good enough to wake his phone.
- **If nothing scores 40+, do NOT notify.** Write one line in the terminal ("Scan clear, nothing
  above threshold") and stop. A notification that says "nothing found" is the fastest way to
  make Hashim start ignoring notifications.
- **Rank the message by the best job, but state the honest spread.** With the floor at 40 a scan
  can push on three 44s. Say so — `"3 borderline (44-51), none strong"` — so he can tell a quiet
  night from a live one without opening anything.
- Desktop toast always. Phone push only when Remote Control is connected on his account.

---

## Step 7 — Persist

Append every scanned-and-rejected job to `references/rejected-jobs.md` as one line:
`<job_id> | <title> | <score> | <reason>`

This is what stops the next hourly run re-surfacing the same rejects. Read this file at Step 1.

Write the full digest to `Danish/scout-reports/YYYY-MM-DD-HHMM.md` so a decision made later can
be traced back to the numbers it was made on.

---

## Hourly automation

`CronCreate` is the only scheduler that reaches the Upwork MCP. Cloud routines (`/schedule`)
cannot — they see only claude.ai connectors, and Upwork is a Claude Code-configured server.

```
CronCreate cron="7 * * * *" recurring=true prompt="Run the job-scout skill."
```

Minute 7, not 0, to stay off the top-of-hour API stampede.

**Constraints Hashim must know, every time this is set up:**
- Session-only. The job dies when this Claude session exits. Nothing is written to disk.
- Fires only while the REPL is idle, never mid-query.
- Auto-expires after 7 days.
- The machine has to be awake and the session open.
