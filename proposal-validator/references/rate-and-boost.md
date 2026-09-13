# Rate and boost rules — autonomous submission

Hashim picks the job. Everything after that, including the bid number and the submit, is handled
without him — **in the sitting where he picked it.** That means the rate cannot be improvised per
proposal. These are the rules.

**Carryover rule (added 2026-09-08, Hashim's correction):** if a proposal was drafted and
validated in a prior session and didn't submit (blocked by something mechanical — a spend
guardrail, not a rejection), do NOT resume and submit it automatically in a new session. Ask first.
State what's changed since it was picked (competition count, connects balance, anything material)
and get a yes. The original pick authorized that sitting, not an indefinite window — conditions
move (a job went from 48 to 116 proposals overnight the one time this was skipped). Same-session
resume (blocked and retried minutes later) is still fully autonomous; only a session/day boundary
triggers the check-in.

**Every submission logs the number AND the reason.** If the reasoning cannot be stated in one
line, the rule is not being followed.

---

## Hourly jobs

**Standard rate: $65/hr.** Six of Danish's last eight proposals. This is the anchor.
**Absolute floor: $40/hr.** Never bid below it. A job whose ceiling is under $40 should not have
survived the scout's hard filters.

```
1. Start at $65.
2. Clamp into the client's stated range.
     range_max < 65  ->  bid range_max
     range_min > 65  ->  bid range_min
     otherwise       ->  bid 65
3. Adjust DOWN toward the field average ONLY when BOTH are true:
     - proposal_count > 25 (crowded)
     - client spend_total < $10,000 (modest buyer)
   Then bid midway between the field average and the clamped number. Never below $40.
4. Never adjust up past the clamped number.
```

### Hourly with NO stated range (added 2026-09-07 — the rule had no branch for this)

Common on consultation and "tell me your rate" postings. There is nothing to clamp to, so use the
**field** as the anchor instead of the client:

```
2b. No stated range:
      field_avg >= 55        ->  bid 65 (standard). Premium field, no discount needed.
      field_avg 40-55        ->  bid 55. Above the field, below standard, defensible on the wedge.
      field_avg < 40         ->  bid 55 anyway, and SAY the field is bidding below the floor.
                                 Do not chase a field that is under-pricing the work.
      no bid stats at all    ->  bid 65 (standard).
    Then apply rule 3 as normal.
```

**Worked examples:**

| Job | Field avg | Bid | Branch |
|---|---|---|---|
| Geospatial building/tent extraction | $58.28 | **$65** | field ≥ 55 → standard |
| Wall replacement | $26.90 | **$55** | field < 40 → floor-protective 55, field under-pricing |

**Why this branch exists:** on the wall replacement job the rule said "start at $65, clamp into the
range" and there was no range. Strict reading gave $65, which would have sat 44% above the highest
competing bid with no client anchor. The number was improvised at $55 instead. Improvisation is
exactly what these rules exist to prevent, so the gap is now closed.

**Worked examples from real submissions:**

⚠ **Arithmetic flag (2026-09-08):** the drone row below says "midway 42-60" but
midpoint(42.40, 60) = 51.20, not 48 — either the historical bid was computed differently, or the
inputs recorded here are wrong. Not resolved; flagging rather than silently trusting either
number. The **AI Solutions Architect** job (2026-09-08) used the literal rule — midpoint(field avg,
clamped standard) — and got $62 from midpoint(59.79, 65) = 62.4, which checks out. Trust the
literal rule text over this drone row until someone reconciles it.

| Job | Range | Field avg | Bid | Why |
|---|---|---|---|---|
| Drone house detection | $30-60 | $42.40 | **$48** | Clamped to 60, then rule 3 fired (43 proposals, $7.8k client). Midway 42-60 — see arithmetic flag above |
| AI Solutions Architect | $40-100 | $59.79 | **$62** | Clamped to 65 (standard, inside range), rule 3 fired (62 proposals, $8.1k client). midpoint(59.79, 65) = 62.4 |
| Basketball court CV | $20-40 | — | **$40** | Ceiling below standard, bid the ceiling |
| Generative video ML | $100-175 | — | **$100** | range_min above standard, bid range_min |
| Camera measurement | $30-59 | $47.58 | **$65** | Hashim overrode above range deliberately. **Human override, not the rule** |

## Fixed-price jobs

**Bid the client's stated budget.** Do not undercut to look cheap; do not pad.

Exceptions, both of which get flagged in the report rather than silently applied:
- Bids cluster far above the stated budget (e.g. $100 stated, $812 average) → the budget is not
  real. Bid the stated number anyway and note that the scope will need renegotiating.
- Scope obviously exceeds the budget → still bid the stated number, and make the letter's
  first-mile offer the smallest viable slice.

| Job | Budget | Bid | Why |
|---|---|---|---|
| Legal-tech NLP | $4,000 | **$4,000** | Stated budget, bids clustered at $3,843 |
| Football calibration | $150 placeholder | **$150** | Client said the number was a placeholder |

---

## Boost

**Default: skip.**

Boosting is a discretionary Connects spend on top of the application. Hashim authorised the
application cost by picking the job; he did not authorise an open-ended auction bid. Skipping is
the conservative default and has been the right call on every proposal this session.

**Do not auto-boost.** When boosting looks genuinely worth it, submit unboosted and say so in the
report:

```
BOOST  Skipped. Top bids were [12 12 11 1] — 13 Connects would clear the field.
       Say the word and I'll boost the next one like this.
```

Boost only when Hashim explicitly asks, for that job or as a standing instruction.

**Research note (2026-09-08, does not change the default):** a vendor blog (bidpilotpro.com, so
read with a sales incentive in mind — but it cited actual numbers) reported 16-20 Connects of boost
lifting reply rate by 1.61pp at roughly $1.94 per extra reply, and Upwork's own placebo-auction
mechanic (organic ranking, no charge, on some posts) confirms boosts affect real ranking, not just
visual position. Kept as a data point, not acted on: skip is still the default because Hashim
authorised the application cost by picking the job, not an open-ended auction. If a genuinely
crowded, high-value job comes up, this is worth surfacing as "boosting has a measured floor here"
rather than a pure guess.

**Reading the auction:** `boost.current_top_bids` in the preview are the real competing bids.
Upwork charges the bid only if the proposal finishes top-4 or the client engages before the
auction closes. Once submitted the bid cannot be changed. Verify with
`list_freelancer_proposals action=get` → `terms.connectsBid`.

---

## Hard stops — never auto-submit

Any one of these stops the pipeline and surfaces to Hashim instead.

| Stop | Why |
|---|---|
| Verdict is **BLOCK** | Fabricated claim or contact info. Never goes out, never silently rewritten |
| **2 rewrite loops exhausted** | The disagreement needs a human, not a third attempt |
| **`totalHired > 0`** on the liveness re-check | Seat is filled. The roofline job went open → hired in 3 days |
| **Connects balance would drop below 50** | Leaves no room to react to an invitation |
| **`connects_cost` > 40** | Unusually expensive application, worth a human look |
| **Job no longer returns** `can_apply: true` | Closed or withdrawn |
| Client rating **below 3.5** | Below the scout's flag threshold; freelancers are reporting real problems |

On a hard stop: do not submit, write the finished letter to the folder anyway, and report exactly
what stopped it and what the options are.

---

## The liveness re-check

**Always re-run `find_jobs action=get` immediately before creating the proposal draft.** Scout data
can be two hours old, and the letter may have taken longer. Confirm:

- `can_apply: true`
- `jobActivity.totalHired == 0`
- `connects_cost` unchanged from what the scout reported
- `connects_balance` still comfortable

This check exists because a real job in this session went from open to `totalHired: 1` between the
letter being drafted and being reviewed.
