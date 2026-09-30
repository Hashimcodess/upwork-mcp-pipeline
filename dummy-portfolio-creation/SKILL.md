---
name: dummy-portfolio-creation
description: >
  Independent skill, not part of the cover-letter pipeline. Run it when you find an interesting
  job post. Capability 1 validates whether the post's problem is worth turning into a public
  portfolio piece: it scores demand, problem interest, marketing value, portfolio gap and
  buildability against a growing ledger of Upwork job posts. Capability 2, after your approval,
  builds an honestly-labelled reference implementation with measured metrics and paste-ready
  Upwork portfolio copy.
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, AskUserQuestion, mcp__upwork__upwork__find_jobs, mcp__upwork__upwork__get_profile, mcp__claude_ai_Figma__generate_diagram, mcp__claude_ai_Figma__create_new_file, mcp__claude_ai_Figma__get_screenshot
---

# dummy-portfolio-creation

Turn a job post worth studying into a portfolio piece worth showing, without pretending the
piece is something it is not.

**Invoke:** `/dummy-portfolio-creation <job URL, job id, or pasted post text>`

| Invocation | Does |
|---|---|
| `/dummy-portfolio-creation <post>` | Capability 1: validate, then stop for your decision |
| `/dummy-portfolio-creation build <slug>` | Capability 2: build a piece that has a BUILD verdict and your approval |
| `/dummy-portfolio-creation status` | List validations and builds, each with its verdict and stage |

**Account:** `org_uid` = `1328310880177278977` (Danish Ashraf). Pass it directly.

## Independence (hard rule)

This skill stands alone. It does **not** call, read, write, or hand off to `cover-letter`,
`proposal-validator`, `job-scout`, `outcome-learner`, `performance-evaluator`,
`pipeline-improver`, or `portfolio-profile-upgrade`. It never appends to `rejected-jobs.md`,
`scout-reports/`, `SESSION-HANDOFF.md`, or any proposal folder. It never writes a cover letter and
never applies to a job.

It **reads**: `Danish/projects/*.md` and the live Upwork portfolio (`get_profile`, read-only), as
the portfolio-gap reference. It **writes**: only its own `data/job-ledger.jsonl` and
`Danish/dummy-portfolio/`. It never calls any Upwork write tool.

If asked for a cover letter, say that is a different flow and stop.

## Step 0 — Intake

1. Take the post from the argument. A URL or id: `find_jobs action=get params={job_id}`. Pasted
   text: use it as given. Nothing supplied: ask for it.
2. Extract, in the client's own wording: the **problem** (what is being built and why it is hard),
   the **inputs and outputs**, any **numbers** in the post, and the **terms** a different client
   would use for the same problem.
3. State the **problem class** in one client-free sentence. Everything after this is about the
   class, not about this client.

`Danish/dummy-portfolio/` is the working folder. If a validation already exists for the same
problem class, show it and ask whether to re-validate.

---

# Capability 1 — Validation

Read `references/corpus-building.md` and `references/scoring-rubric.md` before scoring.

## A1. Build the evidence corpus

Follow the sweep in `references/corpus-building.md`: a class-specific live sweep (about 3 weeks
deep), a dated weekly sweep (reaches at least Jul 1), everything recorded into the ledger with
`scripts/ledger.py add`, then `scripts/ledger.py stats` for the numbers.

The window is **3-4 months by accumulation**. The API cannot look back that far in one go, so the
ledger grows a little with every run. On a young ledger the honest window is short. Say what it
is.

## A2. Portfolio gap

Compare against both references:

1. `Grep pattern "^## Relevance Tags" -A 1` over `Danish/projects` for every project's tags in one
   call, then read the 2-4 closest project files in full.
2. `get_profile action=list_highlights` for the live Upwork portfolio titles.

Name the files and titles compared. Classify NEW / ADJACENT / DOCUMENTED-NOT-SHOWCASED / COVERED.

## A3. Marketing validation

- Searchability: compare the client terms against `get_profile action=get` skills.
- Competitive density: `stats.proposals` from the ledger.
- Differentiation: `WebSearch` for the problem plus "demo", "benchmark", "open source",
  "github"; name what already exists.
- Visual demonstrability: judge what the finished piece would look like.

## A4. Score and write the scorecard

Score with `references/scoring-rubric.md`. **Rate and budget are not scored**: only the
interestingness and usefulness of the problem matter.

Write `Danish/dummy-portfolio/validations/YYYY-MM-DD-<slug>.md` using the template at the bottom of
the rubric.

## A5. Report and stop

Reply in chat, short:

```
VERDICT  BUILD  ·  74/100  ·  confidence MEDIUM
EVIDENCE 27-day class window + sparse 13-week sample · ledger 214 records · older-week counts are lower bounds

DEMAND     21/25   9 unique clients, trend up, 3 industries
INTEREST   17/20   measurable bar (coverage %), hard sub-problem: occlusion
MARKETING  14/20   density 4/5 · differentiation 3/5 · visual 5/5 · searchability 2/5
GAP        15/15   NEW. compared: satellite-imagery-analytics, lidarview / "Object detection with satellite Imagery"
BUILDABLE   7/10   <named dataset, licence>
DEFENSIBLE  4/5    IP SAFETY 4/5

RISKS    <two lines>
IF BUILD <format, effort estimate, what the demo would show>
NEXT     Say "build" to plan it, or skip.
```

**Stop here.** Capability 2 never starts on its own. A BUILD verdict is a recommendation, and the
decision is Hashim's.

---

# Capability 2 — Portfolio creation

Only after a BUILD verdict **and** an explicit go. Read `references/build-guide.md` first and
follow B1-B8 in order:

1. Abstract the brief and fix the success bar before any code.
2. Pick the format, the slug and the effort cap (default 3 working days; ask).
3. Write `plan.md` and **stop for approval**. Ask where the demo will live; name any connector
   needed instead of working around it.
4. Build to the approved plan. Numbers are measured or absent.
5. Produce the assets. Ask before writing to Figma.
6. Write `README.md`, `metrics.md` and `upwork-copy.md`, provenance line first.
7. Final check: re-run the numbers, trace every claim, run the client-residue check, confirm the
   licences.
8. Hand over. State plainly that there is **no Upwork API for adding a portfolio project**, so
   Hashim uploads it himself.

## Honesty line (applies to every output of this skill)

A dummy portfolio piece is legitimate when it is **labelled for what it is**: a demo, a
benchmark, a reference implementation, a study. It is never presented as delivered client work,
never carries a client, logo or testimonial, never uses the client's data, and never states a
number that was not measured on the piece itself. Numbers a stranger can reproduce are the whole
value. See `references/build-guide.md` B7.

## Gates that always require Hashim's explicit yes

1. After validation, before planning a build.
2. After `plan.md`, before writing code.
3. Before writing to Figma or any external account.
4. Before anything is pushed or published. This skill never publishes.

## Files

```
.claude/skills/dummy-portfolio-creation/
  SKILL.md
  references/corpus-building.md   how to gather evidence; measured API limits
  references/scoring-rubric.md    the metrics, weights, gates, verdict, scorecard template
  references/build-guide.md       capability 2, B1-B8
  scripts/ledger.py               add / stats / span over the job ledger
  data/job-ledger.jsonl           created on first run; grows every run
Danish/dummy-portfolio/
  validations/                    one scorecard per validated post
  <slug>/                         one folder per built piece
```
