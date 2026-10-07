# Improvement log

---

## 2026-09-08 17:00 PKT — GIS Expert ArcGIS, clean run, screening-answers pattern worth keeping

**Audited:** proposal `2097293910508724225`, job `2096980885301062573`, $45/hr, no boost, 20
Connects. Same-session pick (Hashim asked for full details on this job twice across the session,
then asked "is it worth applying," got a clear yes, then said go ahead). Match ~55-60%, hybrid
mode. Client is the strongest seen this session by real numbers (146 contracts, 95 hires, 9,137
hours) and had posted this exact job title before with a 5/5 rating from the prior contractor —
that repeat-post detail only surfaced on a second full `find_jobs get` pull, not the first scout
pass. Worth remembering: a client's full work-history sample can turn up a same-title repeat
posting that the scout's summary view won't show.

**Worked well, no gate failures this run.** The wedge was the client's own screening question
(building/road/tree canopy modeling approaches) — research backed all three claims (U-Net for
buildings, topology/graph extraction for roads, instance segmentation for overlapping canopies)
with two real citations. Letter landed at 222 words on the first draft, inside tolerance without
a rewrite loop. Proof bullets (Satellite Imagery Analytics, Well Log Digitization) both verified
cleanly against project files, including getting the Well Log Digitization pipeline ORDER right
(U-Net -> SVM -> YOLO, matching the file exactly) rather than just the ingredient list.

**Screening answers, not just the cover letter.** This job had 5 mandatory screening questions.
Wrote full technical answers for all 5 with the same wedge-first, honest-gap-disclosed standard as
the letter, not shorter throwaway responses. Question 1 (React/.NET/ArcGIS Enterprise/MS SQL) got
an honest "not that combination" answer bridged to real adjacent stack experience (React/Next.js
on FastAPI/Node — verified: Node.js appears in `la-fragrancia.md`, `ideolab.md`, `drive-pulse.md`,
`emotive-tts.md`, so the aggregate claim holds even though no single bullet names those projects).

**Boost note:** only 1 connect would have taken a top slot (only 1 other applicant had boosted at
all). Skipped per the standing default rule anyway and flagged it in the report rather than
deciding unilaterally — consistent with the rule, but this is the cheapest boost opportunity seen
all session and a real candidate for "say the word and I'll boost the next one like this."

**Not changed:** no skill-file edits this run — the pipeline executed as designed with no gaps
found. A clean run is a legitimate outcome.

---

## 2026-09-08 15:00 PKT — AI Solutions Architect, same-session pick, caught a real Gate 1 miss

**Audited:** proposal `2097263791907225600`, job `2097209835808437300`, $62/hr, no boost, 13
Connects. Hashim picked this job explicitly this session after reviewing full job details for two
candidates and asking which was better. Match was genuinely under 40% (approach-led, never-force-
fit) — wedge was a researched claim about AI governance frameworks missing the token-budget/
context-collapse failure layer (60%+ of enterprises hit production agent failures evals never
predicted; 63-incident arXiv catalog on token-budget overruns).

**Found — real catch, not a false positive.** Gate 1 caught the cover letter's StackFuse proof
bullet claiming "per-agent token budget allocation" — StackFuse's actual documented mechanism is
budget allocation between chat history and retrieved context in one shared layer, not a per-agent
split (that's HOKI's shape, not StackFuse's). The letter's own "how I'd approach this for you"
paragraph used "per agent per task" language, and it leaked into the unrelated proof bullet.
Fixed before submit — one rewrite loop, not escalated.

**Also fixed in the same loop:** the hook's structure ("X, and that's not the part that actually
breaks") sat close to the "the real challenge isn't X, it's Y" dead pattern from
`hook-and-cta-guide.md`. Split into two sentences to move away from the shape without losing the
claim.

**Changed:**
- `cover-letter/SKILL.md` Step 4 — added the vocabulary-leak trap: check each proof bullet against
  its project file in isolation, not against the surrounding paragraph's technique vocabulary.
- `rate-and-boost.md` — flagged an unresolved arithmetic mismatch in the drone house detection
  worked example (midway(42.40,60) should be 51.20, table says 48) and added this job's rate
  calc as a second worked example that does check out, so the rule text stays trustworthy even
  with the older row unresolved.

**Not changed:** boost default (skipped — top bids [121,120,7,2], two outliers not worth chasing),
engineer-mode compliance rules (letter was clean on those, zero em dashes, no MiniByte/founder
language, no fabricated Bedrock/Azure/Snowflake/Databricks claims — the letter disclosed that gap
honestly instead).

---

## 2026-09-08 13:37 PKT — Soccer Video Analytics, carryover submission

**Audited:** proposal `2097243015887515649`, job `2096917920317480860`, $50/hr, no boost, 27
Connects. Letter and wedge were written and validated on 2026-09-07 but blocked from submitting by
a session-level automated-spend guardrail (100 Connects/24h, not an Upwork limit). Resumed the next
session, re-ran both mandatory checks — liveness (`can_apply: true`, `totalHired: 0`) and duplicate
(`list_freelancer_proposals` showed no prior proposal on this job) — both clean, submitted via the
standard create → preview → confirm_preview path.

**Worked:** the carryover pattern itself. A letter fully validated one day and blocked only by a
spend guardrail doesn't need re-validating the next session — the liveness/duplicate re-checks are
exactly the right amount of re-verification, not a full re-run of the pipeline. Note for future
sessions picking up a blocked-not-rejected proposal: check those two things, then submit, don't
rebuild.

**Observed:** the 100-Connects/24h ceiling from 2026-09-07 cleared on its own by the next session —
consistent with it being a rolling or calendar-day window, not a standing block. Worth knowing so a
future block isn't mistaken for something that needs a pipeline fix.

**Found — no pipeline gap.** Mechanically clean run. The only soft finding is process, not code: two
scout reports (2026-09-08 01:25 and 02:39 PKT) had run since the last handoff update and hadn't been
folded in yet when this session opened — not a missed rule, just confirms the handoff should be
kept current every session close, which is already the standing instruction. No new rule needed.

**Changed:** `rate-and-boost.md` gained a dated research note (boost measured impact, does not flip
the default-skip). See `research-log.md` 2026-09-08 entry for the two searches run today.

**Not changed:** boost default, rate rules, scout filters — nothing broken to fix this run.

---

## 2026-09-07 15:05 PKT — SILENT BIN. Caught by Hashim. The worst failure class so far.

**What happened:** the Radar & Sensing Engineer job (`2096873902986486790`, Fravek, Sweden) was
scored **35% off the description snippet**, judged below the 40% match floor, and **silently
dropped without telling Hashim.** He asked why it was missed and assumed a cron timing issue. It
wasn't. I saw it in the 14:25 PKT manual scan and said nothing.

**Three failures, compounding:**

1. **Scored from the snippet, not the post.** The full description said *"you might come from
   radar, telecommunications, electronic warfare, radio astronomy, acoustics, GNSS, SDR **or
   another sensing field**"*, named **sensor fusion and GNSS as major pluses**, and closed with
   *"you do not need to be a radar veteran."* The client wrote the post specifically to recruit
   cross-domain. None of that was in the snippet I scored.

2. **Under-weighted adjacency.** Danish has two documented sensor-fusion systems (`gps-denied`
   defence, `aatms` space agency), Kalman-filter target tracking, multi-object tracking with
   trajectory prediction, C++/Python, and GPS-**denied** navigation — literally the GNSS problem
   the client names. True match **55%**, not 35%. The genuine gap is hands-on SDR/RF hardware,
   which the post lists as a requirement.

3. **Anchoring.** The scan in question had already turned up an 84. Having found the winner, I
   rushed the rest. That is exactly when a scan is least trustworthy.

**Re-scored: 57.5.** Borderline, worth surfacing, not an auto-apply. And the decisive factor is
the **client**, not the fit: $3,480 lifetime, 5 hires, zero engineering hiring in their history
(Water Stress Research, patent listing, UX/UI, a hackathon wingman), last contract start Sep 2025,
and **21 invites out with 0 hired**.

**Changed:**
- `SKILL.md` — silent-drop floor moved from **50 to 38**. Everything 38-64 now gets a one-line
  Borderline entry with the reason. Plus an always-surface list (rate tops ≥ $65, serious buyer,
  post invites adjacent backgrounds, <10 proposals, domain Danish has shipped in), and an explicit
  warning that a high score elsewhere must not shorten the rest of the scan.
- `scoring-rubric.md` — new section on **under-scoring cross-domain adjacency**, with the four
  post-signals that mean a client is recruiting sideways, and the instruction to score the problem
  shape rather than the vocabulary.
- `rejected-jobs.md` — entry corrected in place with the real score and the real reason.

**The meta-lesson, and the reason this class is the worst:** over-scoring is loud — it produces a
bad proposal someone reads. **Under-scoring is silent.** Nobody ever sees the job that was wrongly
binned, so the error never surfaces on its own. It only surfaced here because Hashim happened to
notice the job in a later report and asked.

Any filter that removes things without logging *why*, at a threshold where judgment is shaky, will
hide its own mistakes. That is why the floor moved down rather than the scoring being "tuned".

---

## 2026-09-07 14:45 PKT — Geospatial submission (FIRST AUTO-TRIGGERED RUN)

**Rule change, same run:** Hashim made the post-submission flow automatic. `proposal-validator`
Step 6g now invokes this skill the moment a submission confirms, plus a ledger row, plus **one**
combined message rather than two. Saved as `feedback_auto_post_submission.md`.

Cadence guard added so the auto-run stays cheap: **audit every time, outside research at most once
per day** (check the last dated entry in `research-log.md`). Research skipped this run — three
separate research passes already ran today.

**Audited:** proposal `2096896054458929153`, Geospatial AI & CV Expert, $65/hr, 14 Connects,
submitted 24 minutes after the job posted. Scout score 84, the highest yet.

**What went right, and is worth keeping:**
- **First letter to pass every gate on the first pass.** 238 words in band, 0 em dashes, 0 AI
  vocabulary, 3/3 claims verified. No rewrite loop.
- Research upgraded the wedge **twice**: "tents are harder than buildings" → a hard number
  (6px at 50cm, 10px at 30cm) → a better second wedge entirely (cross-settlement generalisation,
  making their own "data-quality assessment" the real gate).
- The arithmetic was computed independently in `awk` *before* searching, and the published figure
  then matched. → **Encoded in `cover-letter/SKILL.md`:** when a wedge rests on a computable
  number, compute it yourself first, then check the literature. An independently derived number is
  defensible in a call, and a disagreement between your maths and the literature is itself a
  finding.

**Gap found and CLOSED — one I had logged and then left open:**
On the wall replacement job (12:35 PKT) I flagged that `rate-and-boost.md` had no branch for
"hourly with no stated range", improvised $55, and logged the gap. **I then did not fix it**, and
the geospatial job hit the same missing branch three hours later. It happened to land on $65
cleanly because the field average was $58, but that was luck, not the rule.

→ Added a **no-stated-range branch** anchored on the field rather than the client:
field avg ≥ 55 → bid 65 · 40-55 → bid 55 · < 40 → bid 55 and say the field is under-pricing ·
no bid stats → bid 65. Both real cases reproduce correctly under it.

**Lesson beyond the fix:** logging a gap is not closing it. A finding written to a log and left
open will resurface, and it resurfaced within three hours here. Findings that name a concrete
missing rule should be fixed in the same run that finds them, not queued.

**Validation datapoint:** the geospatial job went from <5 proposals to 10-15 in 24 minutes.
Direct evidence for the 48-hour age cap and the 2-hour cadence.

---

One dated entry per `pipeline-improver` run. Read before changing anything — it prevents
re-litigating a decision that was already made and reversed.

---

## 2026-09-07 — pipeline built (baseline)

**Audited:** the manual routine that ran 2026-09-01 → 09-06 (7 proposals, 4 submitted).

**Found — the core diagnosis:** the first validator built was a *compliance* checker. It answered
"is this letter clean?" (no em dashes, verified claims, correct length) rather than "will this
letter win?". A letter can pass every compliance gate and still be one of forty forgettable
proposals. Hashim named this directly.

**Changed:**
- `proposal-validator` — added **Gate 0 (will this win)** and made it run first: wedge test,
  substitution test, competitor test, research test, objection pre-empt, six-second test.
- `cover-letter` — Step 2 is now "find the wedge before writing a word", with mandatory WebSearch
  when the wedge rests on a factual claim. Writes `wedge.md` for the validator to check against.
- `job-scout` — added **winnability** at 15 points and a `WEDGE` line on every card. Match tells
  you he can do the job; winnability tells you he can prove it in 200 words against 40 people.
- Root `cover-letter-guide.md` — 4 revisions: bullets now allowed for referenced work (was "no
  bullets"), em dashes zero (was "one max"), length bands cut to 160-240 (was 200-300), Pakistan
  test added.
- Models: `cover-letter` and `proposal-validator` moved to opus; `job-scout` stays sonnet.

**Evidence for the length change:** every letter Hashim approved landed 160-215 words, and two
were sent back explicitly as too long.

**First live catch (roofline letter, same day):** v1 claimed U-Net skip connections beat a
transformer on boundary precision for thin structures. Gate 0d research test contradicted it —
[ViT/SegFormer backbones showed *lower* boundary errors across noise levels](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12468733/)
and [SegFormer beat U-Net variants in a direct comparison](https://dl.acm.org/doi/10.1007/978-3-031-48593-0_8).
The wedge was rebuilt around "the architecture is the least important decision here; your blind
holdout is decided by labeling-spec consistency", which is both defensible and more
differentiating. **Sending v1 would have burned credibility with a client who reads papers.**

**Also caught:** the roofline client asked for a *link* to a self-trained segmentation project.
v1 named a project and gave no link and no acknowledgment, on a post stating "applications that do
not answer all three will not be read". The old process flagged it as a note and moved on.

---

## 2026-09-07 — MISS: applied to a 30-day-old job. Caught by Hashim, not by the pipeline.

**What happened:** submitted proposal `2096864908841508865` to job `2086178149769469238` (wall
replacement, France), posted **8 Aug**, applied **7 Sep**. 21 Connects. Hashim's question: *"why
have you selected an almost a month old job?"*

**Two separate failures.**

**1. The staleness filter had a hole.** It read "posted >24h ago AND 40+ proposals". This job had
9 proposals, so it passed. The filter was designed around the Uma shortlist race, which only
applies to crowded new jobs — it had no concept of a job simply going dormant. A 30-day-old post
with 0 hires is usually solved elsewhere, defunded, or abandoned; Upwork listings stay "open"
indefinitely because nobody closes them.
→ **Added a second staleness rule: >21 days old AND `totalHired == 0` is an auto-discard, and a
low proposal count does not rescue it.**

**2. Client score used lifetime totals with no recency check — the bigger error.**
Scored the client 20/25 on $19,594 spent, 63 jobs with hires, 4.9 from 47 reviews, 13 active
contracts. Never looked at *when* any of it happened. The API had already returned the answer:

```
closed:  started 2025-08-01 · 2025-07-29 · 2025-07-18 · 2025-07-17 · 2025-07-17
open:    started 2025-07-22 · 2025-07-18 · 2025-07-03 · 2025-07-02 · 2025-05-10
```

All ten sampled contracts started May-Aug **2025**. None in 2026. Since the sample is the 5 most
recent by start date in each bucket, there are no newer ones. The 13 "active" contracts are
year-old contracts nobody closed, not ongoing work.

Correct client score was ~8/25, which puts the job at **~61 — below the apply threshold.**

→ **Added a client-recency table to `scoring-rubric.md`:** most recent contract start within
3 months = full marks, 3-12 months = cap at 60% of band, over 12 months = **cap at 8/25 regardless
of lifetime totals**. Plus an explicit warning that a high `contracts_active` count with old start
dates means the client does not close contracts.

**The generalisable lesson:** cumulative metrics never decay. Any signal read from a lifetime
total needs a recency check beside it. Worth auditing the other scoring signals for the same flaw.

**Not fixed, deliberately:** the proposal is already submitted and cannot be withdrawn without
cost. It stays live. The wedge is genuinely strong and the field is weak (9 proposals), so it may
still land — but the odds were worse than scored, and that should have been surfaced to Hashim
before spending the Connects.

**SUPERSEDED same day.** Hashim replaced both staleness rules with a single hard cap: **no job
older than 2 days, no exceptions.** Simpler and closes the hole completely, rather than patching
one shape of staleness at a time. My >21-days-AND-0-hires rule was still reasoning about *why* a
job was stale; his rule removes the question. Saved to memory as `feedback_job_age_2_days.md`.

Enforcement note added to `SKILL.md`: `smart_search mode=most_recent` now passes `days_posted: 2`
and enforces at the API, but **`mode=best_match` ignores dates and `action=search` has no date
filter at all** — results from those two must be age-checked client-side. That asymmetry is the
actual mechanism by which the 30-day job reached scoring.

### Validation run, 2026-09-07 08:08 UTC — rule confirmed, plus an unexpected finding

Re-ran the exact filtered `search` call that had surfaced the 30-day job.

- `smart_search` + `days_posted: 2`: **10/10 within 12.7 hours.** API filter clean.
- Filtered `search` (no date param, client-side check only): **9 of 10 rejected on age.** Ages ran
  3d 11h, 3d 13h, 12d, 13d, 17d, 19d, 22d, 28d, and **29d 12h — the wall replacement regression
  case, correctly caught.**

**Unexpected finding: `client_hires_min` structurally biases toward OLD jobs.** Established clients
accumulate postings, so a hire-count filter surfaces their backlog rather than fresh work. The
"hire-probability scan" of 2026-09-07 07:30, which I presented as the pipeline's best yield, was
mostly stale inventory: its four serious candidates were 18, 20, 22 and 29 days old, and two were
already filled. Under the age cap that entire scan returns nothing.

So the scan I was most pleased with was actually the pipeline's worst failure mode. Warning added
to `SKILL.md`: the hire-count filter is still useful, but the 48-hour cap applies **after** it,
never instead of it.

**Meta-lesson worth keeping:** a filter that improves one signal can silently degrade another.
`client_hires_min` improved client quality and destroyed recency at the same time, and nothing in
the scoring surfaced the trade because age was not a scored dimension — it was a hard filter with
a hole in it.

---

## 2026-09-07 — first fully autonomous run (SDXL LoRA)

**Audited:** proposal `2096753197144711169`, SDXL LoRA Training, $65/hr, 20 Connects. First
proposal submitted end to end with no human read — Hashim picked the job, everything after was
the pipeline.

**Worked:**
- The wedge research found something *sharper* than the hypothesis. Going in, the claim was
  "inconsistency is a dataset problem". The search surfaced that removing the regularization set
  can improve fidelity and style alignment (arXiv 2510.09475), which is contrarian to standard
  advice and gave the letter a second, more differentiating edge. **Research is not just
  verification, it upgrades the wedge.** Worth making that explicit in the cover-letter skill.
- Rate rule fired cleanly and deterministically: $65 standard, clamped inside $50-80, downward
  adjustment correctly did not trigger (needs >25 proposals, job had 13). No improvisation.
- Liveness re-check passed. Cheap insurance, and it has already caught one filled seat.

**Found — false positive in the compliance check:** the automated scan flagged
*"before we scope milestone 2"* as an engineer-mode violation. That "we" meant Danish **and the
client**, not Danish and a team. The rule exists to stop agency framing, not collaboration.

**Changed:** `proposal-validator` Gate 4 now distinguishes the two referents, with examples on
both sides, and notes that rewriting to "you" is usually stronger anyway ("before *you* commit to
milestone 2" puts the decision with the client). Letter was rewritten that way and improved.

**Also:** first draft came in at 255 words against a 180-240 band. Inside the 15% tolerance, but
trimmed to 242 anyway given Hashim has twice flagged length. The tolerance is a ceiling, not a
target.

**Not changed:** dead-job filter still not encoded. Still want a second data point.

---

**Open / not yet done:**
- Mobile push blocked — `mobile push is disabled in /config`, and Remote Control shows offline.
  Two manual steps on Hashim's side. Blocks the notification leg of every skill.
- Dead-job filter not yet added to `job-scout`. The drone job showed **0 of 44 proposals opened**
  after 26 Connects were spent. A `proposals_opened == 0 on jobs >24h old` hard filter is the
  obvious next change — needs one more data point before encoding, since insights lag by an hour.
- `/track-lead` has not been run for any of the three submitted proposals.

---

## 2026-09-14 01:40 PKT — post-submission, Aethera LLM voice/evals advisor

**Audited:** proposal `2099234856592154625`, job `2099226899402997101`, $55/hr, no boost, 21 Connects, balance 91. Scout 78. Same-session pick.

**What worked:** research contradicted the starting wedge hypothesis (nearest-context exemplar retrieval, arXiv 2402.09954 found it performs worst) and it was dropped before reaching the letter, then reused as a "mistake teams make" in Q2. That is the cover-letter Step 2 "research upgrades the wedge" rule working as designed. Liveness re-check caught a moved field average.

**Found, and changed:**
1. Single-cause trap fired a second time (football v1, now "problems 1, 2 and 4 are one gap"). Repeated correction -> explicit rule in `cover-letter/SKILL.md` Step 7: say "most of", not "one gap".
2. Vague attribution x3 ("a CBT study found") failed Gate 2b. -> `cover-letter` Step 7: name the paper in the text.
3. Screening field text differed from the body text (body Q2 had three sub-questions, field had one). -> `cover-letter` Step 7 rule + new Gate 3 row "Screening text drift" in `proposal-validator`.
4. Q3 hardcoded $65 before liveness; field avg moved $34.25 -> $45.09 and rule 2b set $55. -> `cover-letter` uses a `<RATE>` placeholder; `proposal-validator` 6c uses liveness bid stats and fills it; new Gate 3 row "Rate consistency".
5. Bash heredoc with apostrophes failed to parse. -> `cover-letter` Step 8: write files with the Write tool.
6. Attachments invisible to `find_jobs get`. Kitchen CCTV job scored 53 on a $300 three-sentence post whose attached .docx was a 328-camera enterprise RFP. -> `job-scout` Step 4: ATTACHMENT warning line on the card.

**Not changed:** SN3 bullet over-interpretation ("rails-versus-free lives in the graph") was caught by existing Gate 1 as designed. No new rule needed.

**Research:** 1 kept (Uma on Basic plan, reinforces), 2 rejected. See research-log 2026-09-14.

**Open:** Connects 91 and a 1-Connect/12h "Paid invitation badge" drain. About 2 applications left before the 50 floor. Hashim's call whether to top up or turn the badge off.

---

## 2026-09-14 ~02:30 PKT — outcome loop built (Hashim asked)

**Why:** audit of the pipeline found it learns only from caught mistakes, never from results. Improver fires at submit, the moment least is known. Ledger had not recorded outcomes since 2026-09-08.

**Built:**
- `performance-evaluator/data/outcomes.csv` + `scripts/outcomes.py` (add / update / due / summary). Script does all arithmetic.
- Backfilled 16 proposals (7 manual Aug 31 - Sep 4, 9 pipeline Sep 6 - 14). Wedge types read from the actual submitted letters, not from memory. Unrecorded fields left blank.
- Wiring: validator 6g appends a row with `rule_version` = skills repo commit; performance-evaluator Step 0 daily sync; job-scout Step 0 triggers the sync when stale; pipeline-improver Step 1b reads the summary under guards.

**Discovered while building:**
1. `get` returns `room_id` only when the client opened a conversation. The one real per-proposal engagement signal.
2. `list` status filter is unreliable (Declined filter returned Accepted rows). Read status per proposal.
3. Local machine clock runs ~12h behind Upwork timestamps. Mislabelled every proposal age until the script switched to max(local, newest last_checked_utc).
4. First summary buried the most useful rows as "pending". Added `passed_over`: client messaged others, not Danish, after 72h.
5. Guard contradiction: buckets showed [act] at 9 judged while weights_change_allowed=False. [act] now also requires 30 judged overall.

**First read (n=16, judged 9, observe only, no rule changes allowed):** 2 engaged (camera measurement hired, SDXL interview), 5 passed_over, 4 dead, 1 closed, 2 no_response, 2 pending. Both engagements carried a wedge (impossible_spec, misdiagnosis). All 4 wedge "none" letters got nothing. 3 of 4 buried_real_project letters landed on dead jobs, which is a scout problem, not a letter problem. Not significant; logged as observation only.

---

## 2026-09-14 ~03:15 PKT — outcome-learner skill (Hashim: self-evolving, consistency-upgrading)

**Why a separate skill:** outcome logic had been spread across performance-evaluator, pipeline-improver, job-scout and the validator. With three skills able to act on the same numbers, the pipeline could tune itself in contradictory directions. One owner now.

**Built:**
- `outcome-learner/` owns `data/outcomes.csv`, `data/state.json`, `scripts/outcomes.py`, `references/observations.md`, `references/calibration-log.md`.
- `job-scout/references/learned-weights.json`: the scout's component weights and wedge points as data, with baseline kept for bounds. Scout Step 3 reads it; only `outcomes.py learn --apply` writes it.
- Script commands: add, update, due, status, mark-sync, gaps, summary, learn [--apply].
- Guards in code: observe <30 judged (nothing changes), calibrate 30-49 (strong changes only, 90% Wilson intervals must separate, ±3 wedge / ±2 component), confident 50+ (adds ±1 lean). Buckets need 8+ on both sides. 50-150% of baseline, components renormalise to 100, one apply per 7 days, version check flags a REVERT CANDIDATE at 15+ judged per version.
- Scout cards now record COMPONENTS so results can say which part of the score predicted a reply.
- cover-letter reads `wedge_preference`; wedge types are a fixed enum.
- pipeline-improver no longer touches weights; reads observations only.

**Verified:** real data (9 judged) -> stage observe, apply refused, weights untouched, observation written. Synthetic copy (60 judged, in scratchpad, real files untouched) -> impossible_spec +3 on separated intervals, winnability +2 on 0.6 component gap, sum 100, bounds held, second apply blocked by 7-day rule, calibration log written.

**Bug found by the synthetic test and fixed:** version check ordered groups by earliest timestamp with no tie-break; equal timestamps flipped previous/newest. Now ordered by latest submission, version name as tie-break.

**Backfill:** match_pct recovered from scout reports for SDXL 85, wall replacement 70, soccer 70, GIS 55. Geospatial and legal-tech had none recorded; left blank.

---

## 2026-09-14 ~13:35 PKT — Vision AI/CCTV submission (PPE + face-ID wedge)

**Audited:** proposal `2099415357799260161`, job `2099025421965830989` (Vision AI — Integration
with Existing CCTV System, $45/hr, 26 Connects). Scout scored 70, same-session pick.

**Found (all caught in self-review before submit, not by a client — recorded because each is a
repeatable pattern, not a one-off):**
1. Draft came in at 271 words against a 160-220 hybrid band (23% over) because the post embedded 3
   screening questions in the body with no separate API field, and answering them honestly is real
   required content, not padding. The length rule had no allowance for this case, so every job
   shaped like this one will trigger the same trim-and-recheck cycle.
2. Hook opened with "One thing worth flagging early:" — a throat-clearing signpost not on the
   existing dead-pattern list, since it doesn't match any of the six named patterns exactly but
   fails the same test (delays the claim, doesn't earn the second sentence as fast as opening on
   the claim directly).
3. A proof bullet claimed Urban Guard is "running in production" — present tense, but Urban Guard
   isn't among Danish's 5 currently active contracts, so ongoing operation isn't something this
   pipeline can actually verify. "Deployed to production" says the same true thing without the
   unverifiable present-tense implication.

**Changed:**
- `cover-letter/SKILL.md` Step 3: +15% length allowance when 2+ screening questions are embedded
  in the body with no separate field.
- `proposal-validator/SKILL.md` Gate 3: word-count check now measures against the widened band
  first in that case.
- `proposal-validator/SKILL.md` Gate 1: new tense-overclaim guidance — prefer past-tense-safe
  phrasing for any project that isn't a live active contract.
- `cover-letter/references/hook-and-cta-guide.md`: added the throat-clearing signpost pattern to
  the dead-hooks table.

**Research:** skipped, `research-log.md` already has a 2026-09-14 entry (same-day cap).

**Wedge note:** type `unstated_failure` — PPE compliance and face-ID accountability fight over the
same occluded region of the frame (hardhat brim/safety glasses vs. face recognition). Backed by
OCFR 2022 (arXiv:2208.02760). No prior instance of this exact wedge shape in the log; logging it as
a new worked example is left to `winning-patterns.md` only if it converts — too early to add an
unproven pattern there.

**Persisted:** this entry, SESSION-HANDOFF §15, outcome row `2099415357799260161` in
`outcome-learner`, ledger row 2026-09-14 13:30 PKT.

---

## 2026-09-14 23:59 UTC — Principal AI-Native Architect, validator/cover-letter skipped entirely

**Audited:** proposal `2099830059598569473`, job `2099730174664867607` (Principal AI-Native
Software Engineering / Agentic Development Architect), $65/hr, no boost, no attachments, 27
Connects. Scout-surfaced this session at 69 (`scout-reports/2026-09-15-0900.md`). Hashim picked
it directly from the digest and asked for full job details, then a submission note, reviewed it,
asked for one CTA change, then said "proceed."

**Found:**
1. **The whole `cover-letter` → `proposal-validator` chain was never invoked.** The job post said
   "we'll send a technical questionnaire instead of a cover letter," which doesn't map onto either
   skill's normal trigger shape, so the letter got hand-drafted directly in the main conversation.
   Hashim reviewed and edited the CTA live — which inverts the explicit design in both SKILL.md
   files ("Hashim does not read the letter before it goes out," validator owns Gates 0-4). No
   systematic Gate 0 win-check, no Gate 1 claim re-verification pass, no Gate 4 compliance check
   ran. It happened to be fine — the HOKI claims were manually checked against `projects/hoki.md`
   before submission, and there's nothing disintermediation-adjacent in the letter — but nothing
   would have caught it if it hadn't been.
2. **Self-caught tagging error**, not Hashim's: the outcome ledger row was first written with
   `mode: founder`, but the actual letter text uses pure IC framing ("I architected," "I built,"
   no MiniByte/we/revenue language) — i.e. `engineer` mode per the skill's own rule. Corrected via
   `outcomes.py update` before this audit. Cause: picked founder because HOKI's project file says
   "Chief Architect at MiniByte" without checking what mode the actual drafted text landed in.
3. **No proposal folder was created** — first submission this pipeline-improver has audited with
   no `job-post.txt` / `wedge.md` / `cover-letter.txt`. Backfilled for audit-trail consistency.

**Changed:**
- `cover-letter/SKILL.md` (end of Step 8): non-standard submission formats (questionnaire-first,
  "apply by answering these questions in a message," take-home test) still require the full flow
  — proposal folder, Step 2 wedge search, `proposal-validator` invocation. Only the CTA adapts.
- `proposal-validator/SKILL.md` (standing authorisation section): a job that defers to a
  questionnaire/test does not exempt Gates 0-4 from running on whatever text fills the required
  `cover_letter` field.

**Research:** skipped, `research-log.md` already has a 2026-09-14 entry (same-day cap).

**Wedge note:** type `buried_real_project` — most applicants for this role will cite general
AI-coding-tool fluency; the client explicitly wants evidence of engineering controls built around
autonomous decision-making. HOKI's Reward/Penalty Agent (self-optimization from outcome feedback)
and orchestrator-traceable state are a genuine but cross-domain proof (sales-agent platform, not a
coding-agent SDLC) — letter states that gap honestly rather than implying a literal match.

**Flagged, not actioned:** the most literal possible proof for this job type is this very Upwork
pipeline (confidence-gated `learned-weights.json`, `outcome-learner`'s sample-size gating, the
audit trail in `rejected-jobs.md`) — but it isn't a documented project in Danish's portfolio files,
so citing it as personally built would be an identity/role fabrication. Left as an open thread for
`portfolio-profile-upgrade`: if this pipeline is ever meant to be citable, it needs a real,
honestly-scoped project entry first, under whichever name is actually accurate.

**Persisted:** this entry, SESSION-HANDOFF (new 2026-09-14 evening section), outcome row
`2099830059598569473` in `outcome-learner` (mode corrected), `memory/feedback_unusual_format_still_needs_validator.md`,
backfilled `proposals/2026-09-14-principal-ai-native-architect/`.

## 2026-09-15 (00:15 PKT) — Senior Full-Stack Engineer (AI-Native), proposal 2099939795197599745

**Audited:** the submission itself. Scout score 68 held up (StackFuse/HOKI overlap was genuine,
client record was real). Wedge (buried_real_project, StackFuse's own token-budget/context-window
fix) was found first-time by cover-letter Step 2 and needed no rebuild. One clean validator pass,
no rewrite loops, rate came from rule 2 (clamp to range_max $47) with no improvisation.

**Found:** the one genuine gap. The client explicitly wanted someone "not juggling several other
contracts," full-time. Danish currently has 6 ACTIVE Upwork contracts (confirmed via
`list_contracts action=search`). Neither `cover-letter/SKILL.md` nor `proposal-validator/SKILL.md`
had a standing rule for this — it was handled ad hoc this run (disclosed honestly, framed as
small/async, flagged in `wedge.md`) but nothing would have caught a future run that either hid the
conflict or invented a fake hours-per-week number to sound more available.

**Changed:**
- `cover-letter/SKILL.md` Step 7 — new rule: pull `list_contracts` before answering an
  availability/exclusivity question, disclose other work exists, never invent an hours figure.
- `proposal-validator/SKILL.md` Gate 0e — new exclusivity/availability check, REVISE if either
  half (disclosure or non-fabrication) is missing.

**Research:** due today (last entry 2026-09-14). One search kept — Upwork's own blog post
confirming availability is a standalone Uma ranking signal, independent of proposal text — which
is what makes the new rule matter and not just a compliance nicety. One search rejected, no
dated signal found on freelancer community disclosure norms.

**Persisted:** this entry, `research-log.md` 2026-09-15 section, SESSION-HANDOFF (new section
below), outcome row `2099939795197599745` in `outcome-learner`, ledger row in
`Danish/performance/ledger.md`.

## 2026-09-18 02:25 PKT — Audio Processing Service, proposal 2100697244661100545

AUDITED   job 2100684076263057140 ($2,300 fixed, scout 74, submitted 21 Connects, balance 68).
          Wedge survived validation intact. Rate came from the fixed-price rule, not improvised.
          One rewrite loop, both fixes self-caught: a signposting hook ("worth naming early", the
          exact pattern hook-and-cta-guide flags) and "25-style" where the project file says
          "25+ emotional styles".

FOUND 1   `proposal_count` is unstable. The License Plate job read 83 proposals at 14:00 UTC and
          21 at 21:00 UTC, moving its score between 53 and 78 with nothing else changed. Three
          rules key off that field. Scoring a job 25 points lower on one volatile read is how a
          good job gets buried.
CHANGED   job-scout/SKILL.md: take the count from the Step 4 metrics pull, cross-check against
          proposals_tier, score on the lower number when reads disagree by >2x and show both on
          the card, never apply the crowded penalty on a single uncorroborated read.

FOUND 2   No rule covered an aggressively boosted field. This job's auction had top bids
          [101 100 20 17] against a 21-Connect application; the existing surfacing rule missed it
          because recommended_connects was 18, just over the ≤15 threshold.
CHANGED   rate-and-boost.md: new contested-auction line whenever the top bid is 50+, with the
          reasoning that four pinned slots decide placement before the writing is read. Default
          stays skip; 101 Connects is roughly a month of allowance and that call is Hashim's.

FOUND 3   The approach doc came back after six weeks of none (first since the 2026-09-16 rule
          restoration), and the attachment constraint bit in a new way: freelancers cannot open a
          proposal thread, so a doc held back after submit only lands if the client replies first,
          and a submitted proposal cannot be edited to add it.
CHANGED   cover-letter/SKILL.md Step 8: when Hashim is in the loop, offer the upload session
          BEFORE the submit call, not after.

WATCHING  Hashim edited the letter pre-submit for the first time in a while: he cut the sentence
          naming the study and he cut the binary CTA ("Benchmark first, or a 15-minute call?").
          The citation cut left "all 40 configurations" with no antecedent and he accepted a
          7-word source tag when it was pointed out. The CTA cut he kept. One instance is taste,
          not a rule — but if the binary CTA gets cut a second time, the rule in
          hook-and-cta-guide.md is wrong and should be softened to "a clear ask, binary optional".

RESEARCH  1 kept (reinforcing), 2 rejected. Boost cost range from vendor blogs contradicted by the
          live auction on this very job.

PERSISTED research-log · improvement-log · SESSION-HANDOFF · memory

## 2026-09-21 18:25 PKT — CV depth-camera point-cloud measurement, proposal 2102025466902138881

AUDITED  Letter PASSED first time; Hashim then edited it before submit (review requested).
FOUND    1. Proof selection missed the live camera-measurement contract (44464909) because it had no
            projects/*.md file. Hashim asked for "more relevant past projects".
         2. connects_cost rose 10 -> 16 between scout and submit (field 8 -> 20). Validator 6a said
            "unchanged" with no branch for a rise.
CHANGED  cover-letter Step 4: check ACTIVE contracts for in-domain proof (present tense, scope-only).
         proposal-validator 6a: cost rise is expected (Upwork documents it); use the new number,
         tell Hashim if he approved a specific cost this sitting. Hard stop stays > 40.
         projects/camera-measurement-contract.md created (scope facts only, no results).
OBSERVED (once, not encoded):
         - Hashim removed the "haven't shipped on DepthAI" gap line (bonus requirement only). Watch
           for a second instance before changing the admit-limits voice rule.
         - Hashim skipped the approach doc on a HIGH-depth job after it was built.
         - First boosted proposal: 32 Connects into [48 33 32 31] on a 20-proposal, 75%-match field.
           The 4-condition surfacing rule would NOT have fired (recommended 32 > 15). Outcome will
           tell whether the <=15 threshold is too tight.
         - Scout missed the job: posted 3 min after the 11:15 UTC scan.
RESEARCH 1 search. Kept: Upwork states Connects per job "can change during the time the job is posted"
         (quoted via aiproposer/snipework 2026 guides). Rejected: vendor claims of boost 10-60 range.

## 2026-09-21 — HARD RULE change (Hashim)
Overwrote the autonomous-submit authorisation in place: Hashim reviews and explicitly approves every
cover letter before submit; no auto-submission, including unattended/cron runs. Files: README,
proposal-validator SKILL (hard-rule section, PASS verdict, Step 6 header, notify line),
cover-letter SKILL (Step 8 doc-upload, Step 9), rate-and-boost.md header + carryover, outcome-learner flow.

## 2026-09-25 — DJI Matrice 4TD YOLO (2103492318789316609)
AUDITED  scout 2026-09-25-0130 → cover-letter → validator PASS first pass → submitted $400, 9 Connects.
FOUND    1) Scout age math used the machine clock (~12h behind): 48h cutoff and "drops at" times wrong; job went out ~53h old.
         2) Boost option only visible in the create preview, which ran after approval; 1 Connect would have bought a top-4 slot (top bids 3/2/1).
         3) Hashim's "no disclaimer" instruction handled correctly (authority from verified platform facts, no false claim). Encoded as a rule so it repeats.
CHANGED  job-scout/SKILL.md (API-derived "now"), proposal-validator/references/rate-and-boost.md (preview before approval + boost line), cover-letter/SKILL.md (no-disclaimer rule).
RESEARCH skipped by request (light run); last external research 2026-09-21. Wedge research for this job logged in the proposal's wedge.md.

## 2026-09-29 - PDF Extraction + Legal Platform API (2105032852201558017)
AUDITED  scout 2026-09-29-1840 -> cover-letter -> validator PASS after one fix -> submitted $3,000 fixed, 16 Connects, no boost.
FOUND    1) Tier is not a count. Card said "50+ tier"; real field was 170 (172 an hour later). By the scout's own crowd rules the score was 34, below the 40 floor, so Hashim picked from a card that overstated the job by 20 points. Boost auction was also contested (top bids 211/201/200/164).
         2) Notification: tool confirms desktop toast only; skips while terminal is active; phone delivery never confirmed, and the digest said "pushed".
         3) Letter draft said "your attorneys" for an intermediary post (poster is a dev shop, attorneys belong to the law firm). Validator caught it.
         4) outcomes.csv had a blank row, so sync_due stayed true forever.
CHANGED  job-scout/SKILL.md (resolve tier via title search, honest notify wording), proposal-validator/SKILL.md (exact FIELD line in approval message, honest notify wording), cover-letter/SKILL.md (intermediary-post rule), outcome-learner/scripts/outcomes.py (load() skips blank-ID rows).
RESEARCH light: Uma facts and boost mechanics re-checked, nothing new that changes a rule (see research-log).
OPEN     Portfolio highlights lack Riddermark and La Fragrancia (portfolio-profile-upgrade). Approach doc PDF never built, not attached. Remote Control / phone push unverified.

## 2026-09-30 (retail checkout job, proposal 2105310619874095105)
AUDITED  scout 2026-09-30-1915 -> cover-letter -> validator PASS first pass -> Hashim edits -> submitted $1,400 fixed, 15 Connects, no boost, 17 proposals at submit.
FOUND    1) find_jobs get now returns client review comments and, on some jobs, a signed attachment link. The scout skill still said both were unavailable. Verified on Israel client, Fractional CTO client, Algorithm for Stock Calculation (PRD_ML_stocks.docx).
         2) Approach-doc template hardcodes "MiniByte" on cover and header, which engineer mode forbids. First PDF shipped that way, caught on page-1 read, fixed with a local preamble copy.
         3) Hashim supplied proof (Roomi PDF) that has no projects/*.md. It is a proposal, not a shipped system, and the PDF says "we" and Minibyte. No rule covered this.
         4) Scout match 80% vs 65-70% checked against files (no hand-object interaction project anywhere).
         5) `wc -w` counts hyphen bullet markers, so the band check read 4 words high.
CHANGED  job-scout/SKILL.md (attachments and client reviews sections revised), cover-letter/SKILL.md (outside-proof rule + file-verified match note in Step 4, engineer-mode preamble fix in Step 8), proposal-validator/SKILL.md (outside-proof check in Gate 1, bullet-marker note in Gate 3 word count).
NOT CHANGED, n=1: Hashim removed the binary-choice sentence from the CTA (letter shipped with the first-mile ask only). Hashim added a fourth bullet against the max-three rule. Both single instances, so logged, not encoded. If either repeats, make it a rule.
RESEARCH light, nothing new (see research-log).
OPEN     Approach doc PDF and CV not attached (Hashim chose no files). Proposal insights showed proposals_total 23 at 14:34Z against 17 at submit; insights lag and count differently, do not use for the FIELD line.

## 2026-10-01 (LPG cylinder counting, proposal 2105678785336684545)
AUDITED  scout 2026-10-01-1353/1845 -> cover-letter (6 Hashim edit rounds) -> validator PASS -> submitted $15,000 fixed, 19 Connects, no boost, balance 882. 52 proposals by title search at submit, insights showed 46.
FOUND    1) Smart Hail Guard "5,000 devices deployed across the US" was false. It lived in the project file, CLAUDE.md, GEMINI.md, the rubric, the validator's own examples and the embedded CV, and went into about a dozen submitted proposals. The validator marked it VERIFIED because the project file said so. Hashim caught it, not the pipeline.
         2) The cover-letter skill did not know the fixed-price rule: letter quoted $12,500 against a posted $15,000; only the validator's rate rule caught it.
         3) Length: 300-380 words against a 160-220 band because the post demanded projects, architecture, timeline and cost in-body. No rule covered it.
         4) Hashim rejected jargon (homography, metric height) and asked why a cashier in the loop justified a vision system. No plain-language rule existed.
         5) Bullets over three: second time (retail checkout asked four, LPG asked five). Last run logged it as n=1; now it repeats, so it becomes a rule.
CHANGED  cover-letter/SKILL.md (post-mandated sections widen length to ~330, fixed-price price = posted budget, scale claims need provenance, plain language for the client, bullets 2-3 default up to 5); proposal-validator/SKILL.md (scale-claim provenance in Gate 1, ~330 cap for post-mandated sections, bullets up to 5, fixed-price rate consistency).
Earlier this session (already committed 3312e73): Smart Hail Guard hard rule in CLAUDE.md, GEMINI.md, rubric, validator BLOCK, cover-letter skill.
RESEARCH light, nothing new (see research-log).
OPEN     cv-embedded-ai-ml.pdf/.tex, portfolio.pdf and two cv-systems-engineering.tex copies still carry the false claim; needs Hashim's true facts. Other scale claims in the submitted letter (Guardio "commercially deployed", Imagate 1M+ images and 90%+ cost cut, Aethero flight hardware) still rest on project files only: Hashim should mark each CONFIRMED. Job 3 (CAN gateway) drafted and previewed, not submitted. Not yet encoded, n=1: Hashim wanted the cashier-loop logic explained in the letter itself.

## 2026-10-05/06 (ADA takeoff job, proposal 2107201902346067969)
AUDITED  scout 2026-10-05-1738 (score 57) -> cover-letter (wedge unstated_failure, researched from primary sources) -> validator PASS after 5 Gate 1 accuracy fixes -> submitted $55/hr hourly, 16 Connects, no boost, no attachments, balance 633. 26 proposals by title search at submit.
FOUND    1) WebFetch returned garbage for the Caltrans PDF; the facts were only verified because the tool saved the file and pypdf could extract it. Not written down anywhere.
         2) Gate 1 caught the same family of slips twice in one letter: a table figure quoted without its conditions (2% cross-slope, 8.3% slope), a project-file word changed ("scanned" for "raster"), and a convention stated flat. First-pass cover-letter should have caught them.
         3) The rate given to Hashim at job-pick was $65 (24 proposals). By approval the field was 26, rule 3 fired, the rule said $55. A stale suggestion reached the approver. Also the "as of" time quoted in chat was roughly 6h behind the API clock.
         4) rate-and-boost.md said build the preview before approval; the validator hard rule said never create without approval. Contradiction.
         5) Connects: the Availability Badge ("Paid invitation badge") is 14 Connects/week, 1 every 12h. Separately an unexplained -60 (reason null, no job) landed 2, 3, 4 and 5 Oct: 240 Connects, and boost_profile get_status shows no active profile boost. It counts toward the 100-per-24h automated-spend ceiling, leaving room for about two applications a day.
CHANGED  cover-letter/SKILL.md (read the primary source via pypdf; quote numbers with conditions, use project-file wording); proposal-validator/SKILL.md (rate and time re-derived from the 6a pull; approval flow reconciled; whole-window Connects count); proposal-validator/references/rate-and-boost.md (DEFAULT budget type note and re-derive rule; preview-after-first-approval; daily cap counts every Connects row); job-scout/SKILL.md (CONNECTS headroom footer line).
NOT CHANGED  Whether to allow preview-only creation before the first approval is Hashim's call (spends nothing, submits nothing); recorded as open, not decided.
RESEARCH see research-log 2026-10-05.
OPEN     -60 daily charge unexplained, needs Hashim on upwork.com (Ads / profile boost history). Approach-doc PDF not rendered (markdown never approved). 3 of 13 judged engaged; no weights changed (stage observe).
CORRECTION 2026-10-06 (Hashim): the daily -60 Connects are his message-broadcast campaign (Upwork's message boost: charged when the broadcast lands in a client's DMs, opened or not). They were logged above as "unexplained". Not a pipeline fault. Skill wording fixed in proposal-validator, rate-and-boost and job-scout; memory project_connects_drains.md rewritten. Open question: should broadcast spend count toward the 100-per-24h ceiling.
RESOLVED 2026-10-06 (Hashim): the message-broadcast campaign is deliberate and is not part of the 100-Connects-per-24h ceiling. Ceiling now counts application spend only (Job application rows plus proposal boost bids); badge and broadcast are listed separately. Changed proposal-validator SKILL, rate-and-boost, job-scout footer, memory project_connects_drains.md. Supersedes the 2026-10-05 whole-window counting rule.

## 2026-10-06/07 (LiDAR detection and tracking job, proposal 2107554910664073217)
AUDITED  scout 2026-10-06-1402 (score 63, match 85%) -> cover-letter (wedge misdiagnosis, own arithmetic first, SimpleTrack text extracted with pypdf) -> validator with the FIRST real blind read -> Hashim reviewed letter and answers, said final -> submitted $60/hr, 20 Connects, no boost, no attachments, balance 551. 50 proposals at submit (25 at scout).
FOUND    1) Blind read worked as designed: it flagged the two gaps that were real (no OS in Q1, Q4 part plan) and one that was not (no VLS-128 claim, which the project files cannot back). Both real gaps are facts only Hashim holds; the draft had no step asking for them before the validator ran.
         2) First-pass slip caught by self-check, not by a gate: Q4 said Hungarian matching "per SimpleTrack" while the paper says distance metrics pair better with greedy. Fixed against the extracted text before the blind read. The existing "read the primary source" rule covered it; no new rule.
         3) Job age at submit was 15.4 h. Insights showed 11 shortlisted, 0 opened, so the proposal arrived after Uma's roughly six-hour shortlist. Single observation.
         4) Second job in a row with approach-doc.md and no rendered PDF (markdown never approved).
         5) Scout labelled the wedge unstated_failure; cover-letter recorded misdiagnosis. The outcome row uses misdiagnosis (what the letter did). Scout wedge points are a prediction, not the label, so left alone.
CHANGED  cover-letter/SKILL.md (Step 4: ask Hashim for personal-experience facts the files lack, before the validator; Step 8: record md-only doc decision in wedge.md); proposal-validator/SKILL.md (report AGE and insights.shortlisted next to FIELD).
NOT CHANGED  No scout weights, no wedge preference (outcome stage observe, 14 rows now, learning gated at 30).
RESEARCH see research-log 2026-10-06.
OPEN     Q1 OS and Q4 tracker design for AATMS/LiDARView still unknown; if Hashim supplies them, put them in projects/aatms.md and lidarview.md so future letters inherit them. Watch whether the proposal is opened given it joined after the shortlist.

## 2026-10-07 (ESP32 dermatoscope job, proposal 2107789502694899713)
Audited: scout card, letter v1 to v5, screening answers, validator loop, blind read, submit flow.
Found and changed:
1. Scout under-read hardware jobs (35% vs ~50% file-verified; VR Glasses, FabSky, Arm Lift, Aethero missed). scoring-rubric.md: new "Physical hardware / optics / fabrication" domain table plus the gaps that stay gaps.
2. Blind read flagged forced "that's your X" tie clauses as AI tells. cover-letter/SKILL.md: tie only where the overlap is literal (revised, was: always tie).
3. Gate 1 caught "printed reference" (file: credit card) and a 52 mm iPhone 2x (Pro is 48 mm). proposal-validator standing traps 7 and 8.
4. Boost approved after preview forced a rebuild. rate-and-boost.md: rebuild rule, when the approval carries over, and BOOST line in the first approval message.
5. Hashim: no committed timeline, overlap by mutual agreement. Memory feedback_no_committed_timeline.md.
Rejected: none from outcomes (13 of 30 judged, observe). Research: no rule change.
