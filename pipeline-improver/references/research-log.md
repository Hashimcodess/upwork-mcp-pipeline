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
