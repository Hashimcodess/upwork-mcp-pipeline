---
name: portfolio-profile-upgrade
description: >
  Recommend and build portfolio pieces and profile changes that improve Uma matching and
  client conversion. Reads demand from live Upwork jobs and session history, proposes what
  to add, builds the approved pieces into the Portfolio folder, and stages profile keyword
  and copy changes for approval before any write.
model: opus
disable-model-invocation: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, PushNotification, mcp__upwork__upwork__get_profile, mcp__upwork__upwork__update_profile, mcp__upwork__upwork__confirm_preview, mcp__upwork__upwork__find_jobs, mcp__upwork__upwork__list_freelancer_proposals, mcp__claude_ai_Figma__generate_diagram, mcp__claude_ai_Figma__create_new_file, mcp__claude_ai_Figma__get_screenshot
---

# portfolio-profile-upgrade — make the profile match the demand

**Account:** `org_uid` = `1328310880177278977`.

Everything lands in `Danish/Portfolio & profile upgradation/`:
- `Portfolio/` — one folder per project, ready to paste into Upwork
- `profile upgradation/` — staged title, overview, and skills changes

**Nothing goes live without Hashim's approval.** Recommend, get a yes, then build.

---

## Part A — Portfolio

### A1. Read the demand

Three sources, weighted in this order:

1. **Live Upwork jobs.** Danish's actual feed, not a generic market view.
   ```
   find_jobs action=smart_search params={mode:"best_match", limit:10}
   find_jobs action=search params={query:"computer vision drone embedded AI", sort:"recency", limit:10}
   ```
   Record which capabilities keep appearing across jobs he wants but keeps scoring 40-70% on.
   **A recurring 55% match is a portfolio gap, not a skills gap.**

2. **Competitor field data.** From `list_freelancer_proposals action=get` on recent proposals:
   `applicants_top_skills` shows what the winning field is actually selling. Skills that keep
   appearing there and are absent from Danish's profile are the highest-signal gaps available.

3. **Current portfolio.** `get_profile action=list_highlights` returns existing portfolio projects
   and certificates. Never propose something already there.

Then check what is trending:
```
WebSearch: "most in demand AI freelance skills <current year>"
WebSearch: "Upwork computer vision jobs trending <current year>"
```

### A2. Score the gaps

For each candidate piece:

| Signal | Question |
|---|---|
| **Demand** | How many jobs in the last 30 days would have scored higher with this piece? |
| **Uma match** | Does it carry the exact terms clients use in their posts? |
| **Credibility** | Can Danish genuinely build and defend it in a call? |
| **Effort** | Days to produce something that stands up to a technical client |
| **Gap size** | Is this actually missing, or already covered by an existing project? |

Recommend **2-3 pieces maximum**. A shortlist Hashim will act on beats a list of ten he won't.

### A3. The honesty line — read this before building anything

Portfolio pieces do **not** have to be paid client work. A demo, a benchmark study, a reference
implementation, an open-source tool are all legitimate portfolio entries, and building one to meet
visible demand is a normal, smart thing to do.

What matters is that the **framing matches reality**:

| Legitimate | Not legitimate |
|---|---|
| "Demo — reference implementation I built to show the approach" | Presenting a demo as delivered client work |
| "Benchmark study, methodology and results published" | Inventing a client, a logo, or a testimonial |
| "Open-source tool, code linked" | Fabricated metrics ("reduced costs 40%") from a system nobody ran |
| Real numbers measured on the demo itself | Numbers copied from a paper as if Danish produced them |
| A real project written up more clearly | An NDA project with invented specifics filled in |

This is not squeamishness, it is risk management. Upwork can remove a profile for
misrepresentation, and a technical client who catches one invented metric discounts everything
else on the page. Danish is Top Rated Plus; that asset is worth more than any single piece.

**The good news:** a well-built demo with honestly-measured numbers converts better than a vague
claim about client work under NDA, because the client can actually see it.

Every generated piece carries a `provenance` line in its README stating exactly what it is.

### A4. Build the approved pieces

Per project, create `Portfolio/<slug>/`:

```
README.md          provenance, what it is, what it proves
upwork-copy.md     title (<=70 chars), the description to paste, skill tags
assets/            diagrams, screenshots, charts
code/              if it is a code piece
metrics.md         what was measured, how, on what hardware. Real numbers only
```

**`upwork-copy.md` is the deliverable.** It is what Hashim pastes. Write it to Upwork's actual
portfolio form: a title, a description, and the role. Front-load the terms clients search on.

**Assets.** Figma MCP is connected and can generate real diagrams (`generate_diagram`,
`create_new_file`, `get_screenshot`). Architecture and pipeline diagrams read as far more
professional than a wall of text and they are cheap to produce. Note that generating them creates
real files in Hashim's connected Figma account.

If a piece needs something not available (a video walkthrough, a live hosted demo, a real dataset),
**say so and ask.** Hashim has offered to provide any MCP or connector needed — name the specific
thing rather than working around it with something weaker.

### A5. Upload — the hard constraint

**There is no Upwork API for individual-freelancer portfolio projects.** `update_profile` covers
title, overview, availability, skills, employment, languages, education, and other experience.
Portfolio is not in that list, and the only portfolio tool on the server is agency-scoped, which
does not apply to this account.

So: everything is prepared to paste, and Hashim uploads at
**upwork.com → Profile → Portfolio → Add Project**. Say this plainly every time. Do not imply an
automated upload is coming.

---

## Part B — Profile upgradation

### B1. Read current state
```
get_profile action=get
```
Capture title, overview, current skills (max 20), employment, languages, education.

### B2. Find the keyword gaps

Cross-reference three sources:
- Terms appearing in jobs Danish wants, in the client's own wording
- `applicants_top_skills` from proposal insights — what the competing field lists
- Upwork's skill ontology (`set_skills` resolves names against it; unresolved names are rejected,
  never guessed)

**The 20-skill cap forces trade-offs.** Adding means dropping. Justify both sides of every swap.

Precedent from 2026-09-02: added PyTorch, Generative AI, Embedded C, NLP; dropped Research &
Development, Unix Shell, Electrical Engineering. Title and overview were left alone deliberately.

### B3. Stage the recommendations

Write to `profile upgradation/YYYY-MM-DD-recommendations.md`:

```
## Skills (20 cap)
KEEP    [current list]
ADD     PyTorch          seen in 7 of 12 target jobs, absent from profile
DROP    Unix Shell       0 target jobs, generic
NET     20/20

## Title (max 70 chars)
CURRENT  <exact current>
PROPOSED <new>
WHY      Uma matches the title against job requirements. "Computer Vision"
         appears in 9 of 12 target jobs and is not in the current title.

## Overview (max 5000)
CURRENT  <first 200 chars ...>
PROPOSED <full text>
CHANGES  Front-loaded CV/drone/embedded terms into the first 150 chars, which
         is what shows in search results before the fold.

## Not recommended
<things considered and rejected, with the reason>
```

**Never write to the profile without explicit approval.** `update_profile` returns a preview;
present it, get a yes, then `confirm_preview`. Title and overview are the most visible things on
the account — Hashim has previously been explicit about leaving them alone, so treat any change
there as needing a clear yes, not an assumed one.

### B4. Apply
On approval, per change:
```
update_profile action=<update_title|update_overview|set_skills|...>
confirm_preview  type=<profile_update_title|profile_update_overview|profile_set_skills|...>
```
`set_skills` replaces the **entire** set — always pass the full revised list, not just additions.

Record what went live, with the date, in the recommendations file.

---

## Output

```
PORTFOLIO & PROFILE — 2026-09-07

DEMAND READ   12 target jobs, 30 days
GAPS          1. Real-time video analytics demo — 5 jobs at 55-65% match would
                 have scored higher. Nearest existing piece is Trackzella (no
                 public artifact).
              2. Roofline/aerial segmentation — 3 jobs, and the wedge research
                 is already banked from the roofline proposal.

RECOMMEND     Build 1 and 2. Both are demos, both labelled as demos, both with
              measured numbers on stated hardware.

PROFILE       ADD PyTorch, Object Detection · DROP Unix Shell, R&D
              Title change proposed, needs explicit approval
              Overview: front-load CV terms into first 150 chars

STAGED        Portfolio & profile upgradation/profile upgradation/2026-09-07-recommendations.md
NEEDS YOU     Approve the two pieces, then upload manually (no portfolio API)
```

Notify when recommendations are ready for review, and again when built pieces are ready to paste.
