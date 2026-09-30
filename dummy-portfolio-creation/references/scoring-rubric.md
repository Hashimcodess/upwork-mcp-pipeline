# Validation rubric

Score 0-100. **Rate and budget are deliberately not scored.** Hashim's instruction: only an
interesting problem statement matters. A post can pay $10 and still be the right thing to build
if the problem is good, so nothing here penalises it.

| # | Metric | Weight |
|---|---|---|
| 1 | Demand and recurrence (how useful the use case is) | 25 |
| 2 | Problem interest | 20 |
| 3 | Marketing validation | 20 |
| 4 | Portfolio gap | 15 |
| 5 | Buildability on public data | 10 |
| 6 | Defensibility | 5 |
| 7 | IP safety | 5 |

## 1. Demand and recurrence (25) — from ledger `stats`

| Part | Points | How |
|---|---|---|
| Recurrence | 0-18 | `unique_clients` in the window. 0 → 0, 1-2 → 4, 3-5 → 8, 6-9 → 12, 10-14 → 15, 15+ → 18 |
| Trend | 0-3 | Up 3, flat 2, not scored (window under 28 days) 1, down 0. Never call "down" off a thin older half |
| Industry breadth | 0-2 | Distinct industries among the matched posts. 3+ → 2, 2 → 1, 1 → 0. Transferable beats one vertical |
| Buyer reality | 0-2 | Median client spend of matched clients ≥ $5k, or ≥ 33% of them ≥ $5k → 2. ≥ 15% → 1. Else 0 |

Report `confidence` (LOW / MEDIUM / HIGH) from the script beside the score. LOW does not change
the score. It changes how loudly the verdict is qualified.

## 2. Problem interest (20) — judged, each part justified in one line

| Part | Points | Question |
|---|---|---|
| Measurable success bar | 0-6 | Does the problem have a number a stranger could check (coverage %, latency, error in cm, F1)? |
| Non-commodity | 0-6 | Is it more than glue, CRUD, prompt wiring or platform assembly? |
| Hard sub-problem | 0-5 | Is there one part a peer engineer would find genuinely interesting to solve? |
| Generalises | 0-3 | Does the problem survive removing this client's specifics? |

## 3. Marketing validation (20) — four parts of 5

| Part | Full marks | Evidence |
|---|---|---|
| Searchability | 5 = the piece would carry frequently-used client terms that the profile lacks; 3 = partial; 1 = terms already fully on the profile; 0 = terms do not map to Upwork skills | Term frequency in matched posts versus `get_profile action=get` skills and portfolio titles |
| Competitive density | median proposals ≤ 15 → 5; 16-30 → 4; 31-50 → 3; 51-80 → 1; > 80 → 0 | `stats.proposals`. If only tiers exist, use the tier and say so |
| Differentiation | 5 = few public demos with measured numbers exist; 3 = several generic ones; 1 = saturated with tutorial-level content | `WebSearch` for the problem plus "demo", "benchmark", "open source", "github". Name what you found |
| Visual demonstrability | 5 = readable in one image or GIF in ten seconds; 3 = needs a caption; 1 = terminal output only | Judge from the deliverable, not the topic |

## 4. Portfolio gap (15)

Compare against **both** references, as Hashim specified:

1. `Danish/projects/*.md` (the 50-odd documented projects). Pull every file's tags in one call:
   `Grep pattern "^## Relevance Tags" -A 1` across `Danish/projects`. Then read the 2-4 closest
   files in full.
2. The live Upwork portfolio: `get_profile action=list_highlights` (titles only, currently 10).

| Result | Points |
|---|---|
| **NEW**: no existing project covers more than ~30% of it | 15 |
| **ADJACENT**: an existing project covers part of it, and the piece adds a distinct capability | 10 |
| **DOCUMENTED, NOT SHOWCASED**: a project file covers it but nothing on the Upwork portfolio does, so a public artifact would still add proof | 7 |
| **COVERED**: an existing project already covers it and is on the Upwork portfolio | 0. Gate: SKIP unless a clearly stronger version is argued in writing |

Name the specific project files and portfolio titles compared. "Nothing similar" with no names is
not an answer.

## 5. Buildability on public data (10)

| Part | Points | Question |
|---|---|---|
| Data | 0-4 | Is there a public dataset whose licence allows portfolio use, or can honest synthetic data be generated? Name it |
| Compute and time | 0-3 | Does it fit the effort cap (default 3 working days) on hardware Danish has? |
| Tooling | 0-3 | Are the models and libraries available and stable? |

## 6. Defensibility (5)

5 = direct precedent in a project file, so Danish can defend every choice on a call. 3 = adjacent
precedent. 1 = a new skill Danish would be learning on the job. Score 2 or below is called out
in the verdict, because a piece that cannot be defended in an interview costs credibility.

## 7. IP safety (5)

5 = the problem class is generic and a public data substitute exists. 3 = works only with
synthetic or simulated data. 0 = depends on the client's private data, schema, benchmark or
scoring harness.

## Gates (any one forces SKIP, whatever the score)

- **IP-unsafe**: the problem only exists in the client's private data or system.
- **Already covered**: score 0 on portfolio gap and no stronger-version argument.
- **Cannot be shown honestly**: no way to produce measured output on public data.
- **Harmful class**: detection-evasion, deception, or surveillance-abuse tools. Do not build a
  showcase for them, and say why.

## Verdict

| Score | Verdict |
|---|---|
| 70+ | **BUILD** |
| 50-69 | **BUILD LATER**: hold it, and re-validate when the ledger has grown |
| Under 50 | **SKIP** |

State the evidence window and confidence next to the verdict every time. A BUILD on LOW
confidence is a legitimate result, but it must be labelled as one.

## Scorecard template (`Danish/dummy-portfolio/validations/YYYY-MM-DD-<slug>.md`)

```
# Validation: <working title>
VERDICT   BUILD | BUILD LATER | SKIP      SCORE  NN/100
EVIDENCE  window <n> days (requested 120) · ledger <n> records, <oldest> to <newest> ·
          confidence <LOW|MEDIUM|HIGH> · older-week counts are lower bounds
SOURCE    <job id / URL>  (private: never copied into the deliverables)

PROBLEM CLASS  <one generic sentence, client-free>
TERMS          <client wording used for the sweep>   EXCLUDED  <false-positive words>

1 DEMAND       NN/25  unique clients <n> · trend <...> · industries <...> · median client spend <$>
2 INTEREST     NN/20  bar <n>/6 · non-commodity <n>/6 · hard sub-problem <n>/5 · generalises <n>/3  (one line each)
3 MARKETING    NN/20  searchability <n> · density <n> (median <x> proposals) · differentiation <n> · visual <n>
4 GAP          NN/15  NEW | ADJACENT | DOCUMENTED-NOT-SHOWCASED | COVERED — compared: <files> / <portfolio titles>
5 BUILDABLE    NN/10  data <named dataset + licence> · compute <...> · tooling <...>
6 DEFENSIBLE   NN/5   <precedent project>
7 IP SAFETY    NN/5   <why>

GATES     none tripped | <which>
RISKS     <two or three lines>
IF BUILD  proposed format · effort estimate · dataset · what the demo would show
```
