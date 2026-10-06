# Research log

What outside research was read, what was kept, what was rejected and why. Read this first so the
next run does not re-read the same low-value sources.

Filter: **dated · sourced or measured · does not contradict our own observed data · ToS-safe ·
would actually change a rule.**

---

## Platform facts currently encoded (verified, load-bearing)

| Fact | Where it lives | Confidence |
|---|---|---|
| Specialized Profiles retired 2026-05-28; one main profile, surfaced dynamically per job | root `CLAUDE.md` | High — half the internet still describes the old system, so re-check anything that assumes it |
| Uma Recruiter machine-ranks proposal text **and screening answers**, delivers a ranked shortlist within ~6h of posting | root `CLAUDE.md` | High — drives the "answer screening questions properly" and "mirror exact wording" rules |
| Attachments are not documented as a Uma scoring input | root `CLAUDE.md` | Medium — so credibility must live in the text, not the PDF |
| ~37% of Upwork proposals are AI-assisted | root `CLAUDE.md` | Medium — the basis of the whole wedge strategy |
| Boost is a Connects **auction**, charged only if you finish top-4 or the client engages | observed directly in `manage_proposals` previews | High — first-party, from the API |
| Disintermediation policy: no contact details pre-contract, enforcement lands on the freelancer | root `CLAUDE.md`, validator Gate 4 | High |

## Observed directly (outranks any blog post)

| Observation | Source | Date |
|---|---|---|
| Client had opened **0 of 44** proposals on a live job | proposal insights, job 2096348 | 2026-09-06 |
| Competing field on a $30-60/hr CV job averaged **$141k earnings, 0.994 JSS, 28 jobs, 5.5 years** | proposal insights | 2026-09-06 |
| Insights refresh hourly and lag a fresh submission | API note | 2026-09-06 |
| Client review **text** is not exposed by the API at all | `find_jobs get` schema | 2026-09-04 |
| Portfolio projects have **no write API** for individual freelancers | `update_profile` schema | 2026-09-07 |
| Boost bids on real jobs ranged 1-180 Connects; often the top bid is trivially low | `manage_proposals` previews | 2026-09-06 |

## Rejected

| Source type | Why rejected |
|---|---|
| Undated "Upwork tips" listicles | Cannot tell if they predate the May 2026 profile change |
| Course-selling blogs | Incentive to overclaim, never publish real denominators |
| "Personalize your proposal" advice | True but non-actionable; already covered better by the wedge |
| Reddit anecdotes with no numbers | Heavy survivorship bias; keep only posts with counts |

## 2026-09-08 findings

| Finding | Source | Verdict |
|---|---|---|
| Uma's shortlist ships within ~6h of posting; a proposal after that window "was never in that race" — response speed is a visibility factor, not just a scoring input | Upwork's own Uma blog post + secondary summaries | Confirms the existing 2-day job-age cap and 3x/day-ish scout cadence direction. No rule change — already encoded. |
| 16-20 Connects of boost measured at +1.61pp reply rate, ~$1.94/extra reply; Upwork's placebo-auction mechanic (unbilled, organic-ranked on some posts) confirms boosts move real ranking, not just visual position | bidpilotpro.com (vendor blog, sells a bidding tool — read with that incentive in mind, but cites real numbers) | Logged as a data point in `rate-and-boost.md`. Did NOT flip the default-skip boost rule — Hashim's authorisation covers the application, not an open-ended auction. |

## Open questions worth researching next run

- Does boosting affect the machine ranking pre-auction-close, or only after (i.e. does it help
  even on jobs the client reads within the first hour)? The 2026-09-08 finding answers "boosts do
  something real" but not the timing question.
- Is there a measured relationship between profile keyword density and Uma match rate?
- What actually moves JSS on a Top Rated Plus account, and what does a declined proposal cost?

## 2026-09-14 findings

- KEPT (reinforces, no rule change): Uma Recruiter reportedly moved from Business Plus to the Basic client plan in May 2026, so the AI shortlist now applies to almost every client. Source: UpAlerts guide (third-party, not yet confirmed on an Upwork page). Also stated there: all proposals stay visible, the shortlist is a nudge, not a gate. Consequence: screening answers are a ranking input on nearly every job, which the existing screening-answers guide already assumes. https://upalerts.app/blog/uma-recruiter-shortlist-guide
- REJECTED as a rule, logged as a data point: GigRadar claims reply rate 11.86% for bids sent 3-4 minutes after posting vs 6.91% at 5-6 minutes. Vendor sells auto-bidding, so heavy incentive bias, and no date on the dataset. Would only matter for scout cadence, and the pipeline cannot hit a sub-5-minute window with a researched wedge anyway. https://gigradar.io/blog/upwork-algorithm
- REJECTED: generic 2026 "algorithm guide" posts (jobbers, giguphq, snipework) with undated percentage weights for JSS/keywords. Unsourced.

## 2026-09-15 findings

- KEPT (new rule): "Availability is a live signal, so a profile marked as not available for new
  work is being scored against one that is, and no amount of portfolio makes up for that."
  Confirms availability/exclusivity screening answers are a standalone Uma ranking input, separate
  from proposal text quality. Source: upwork.com/blog/uma-recruiter-how-we-built-an-agentic-solution-to-talent-matching-and-hiring
  (Upwork's own blog, dated 2026). Applied to `cover-letter/SKILL.md` and `proposal-validator/SKILL.md`
  after the Senior Full-Stack AI-Native job surfaced a real conflict (client wants no other
  contracts, Danish has 6 active).
- REJECTED, no signal: searched r/Upwork for freelancer disclosure norms on multiple concurrent
  contracts vs a full-time ask. No dated community discussion surfaced, only generic Upwork
  contract-writing pages and unrelated financial-news noise. Nothing to log.

## 2026-09-17 findings

- REJECTED, and worth recording because direct observation beat it: multiple 2026 guides
  (zenlance.net/upwork-boosted-proposals, gigradar.io/blog/upwork-algorithm) state boosting to the
  top four "costs 25 to 40 Connects per bid". The Audio Processing Service preview the same day
  returned real `current_top_bids` of [101, 100, 20, 17]. The published range is not a ceiling and
  is not reliable. Rule added to `rate-and-boost.md`: trust the preview's own bids, never a blog's
  range.
- KEPT (reinforces existing rule, no change): boosted proposals are pinned above the organic list
  in the client's Proposal Manager, so on a contested job placement is settled before the letter is
  read. Already the basis of the crowded-field warnings; now also the basis of the contested-auction
  report line.
- REJECTED again (third time): the gigradar "bid within 3-4 minutes" reply-rate claim. Same vendor,
  same incentive, still undated. Flagging here so a fourth run stops re-reading it.

## 2026-09-21
- KEPT: Connects cost per job is dynamic while the job is live (Upwork's own wording, quoted in 2026
  guides at aiproposer.com and snipework.com). Matches direct observation 10 -> 16. Encoded in validator 6a.
- REJECTED: "boosts cost 10-60 Connects" (vendor blogs); contradicted by observed 100+ bids on 2026-09-18.

## 2026-09-29
- KEPT: nothing new. Upwork's own pages and blog again confirm Uma ranks proposal text plus screening answers and delivers a ranked shortlist; already encoded.
- REJECTED: gigradar / upwex / snipework / aiproposer Connects-and-boost cost guides ("14-25 Connects, boosts past 50"). Vendor blogs, and the observed top bids on this job were 211/201/200/164, far above their ranges. Trust the preview's current_top_bids.

## 2026-09-30
- KEPT: nothing new. Search for a September 2026 proposals or Uma policy change found none; Upwork status page showed only resolved outages (Sep 9, Sep 13).
- REJECTED (again): vendor pages (gigradar, upwex, aiproposer, jobbers, getmany) claiming boosts cost "25-40 Connects". Contradicted by this job's real auction: top bids 31 / 30 / 15 / 12, and 13 cleared a top-4 slot.

## 2026-10-01
- KEPT: nothing new that changes a rule. Search confirms Uma (launched Oct 2025, moved to the Basic plan on May 5, 2026) reads proposal text plus screening answers, and that repetitive proposals are penalised. Already encoded.
- UNVERIFIED, not encoded: vendor blogs (snipework, uphunt, upalerts) say that on jobs where the client turns it on, completing an Uma AI video interview is required before a proposal can be submitted. One source class, no Upwork primary page. If a scanned job's `find_jobs get` shows such a requirement, add it as a scout card flag then.
- REJECTED: no October 2026 policy announcement exists yet in search results; the "AI agents as a hiring category" piece (memvers.com) is market commentary, not a rule.

## 2026-10-05
- KEPT (from Upwork's own tool, strongest source): `boost_profile get_status` shows the "Paid invitation badge" is the Availability Badge, ON since 2026-07-31, price 14 Connects, renewed by the system, next renewal 2026-10-06T02:59Z, no active profile boost ad. That explains the -1 every 12h and rules out an active ad as the cause of the -60 rows.
- UNVERIFIED, not encoded as fact: upwex.io says a boosted-profile click can cost "60 to 70+ Connects", charged per client click with an optional daily limit. Vendor blog, official support pages return 403 to WebFetch, and get_status shows no ad now. Fits the -60 pattern but is not proven; Hashim to check ad history on upwork.com.
- KEPT: Uma availability to all clients since 2026-05-05 and screening answers scored (upalerts, snipework, already encoded).
- REJECTED: uphunt / zenlance Connects pricing pages (price per Connect, not a rule change); nothing new on Uma ranking this month.
- CORRECTION 2026-10-06: the -60 daily charge is Hashim's message-broadcast campaign, not a profile ad. A search result titled "How to Boost a Message for freelancers" (support.upwork.com) exists and fits, but the page returned 403 and was not read. `boost_profile get_status` does not report it.

## 2026-10-06
Query: Upwork Uma recruiter shortlist proposals update October 2026. Result: nothing newer than the May 2026 expansion of Uma Recruiter shortlisting to the Basic plan (shortlist about six hours after posting; Upwork internal testing Nov 2025 to Mar 2026: shortlist users hired 30% more often, filled jobs 11% faster). Vendor blogs (snipework, upalerts, appalach.ai) repeat the same facts; none carries new dated numbers. No rule changed. Rejected as low-value: generic "how to win on Upwork 2026" proposal-tip blogs (undated advice, course-selling tone). Our own insights (11 of 49 shortlisted before our submit) are the stronger evidence for the timing observation.
