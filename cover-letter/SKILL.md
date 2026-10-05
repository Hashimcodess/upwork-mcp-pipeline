---
name: cover-letter
description: >
  Write an Upwork cover letter for Danish from a chosen job post. Finds the technical wedge,
  researches it, matches portfolio projects honestly, writes a humanized hook and CTA, lists
  referenced work as bullets, saves to a dated folder, hands off to proposal-validator.
model: opus
disable-model-invocation: false
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, mcp__upwork__upwork__find_jobs
---

# cover-letter — write the letter that wins

**Account:** `org_uid` = `1328310880177278977`.

## The one thing that matters

Every proposal Danish has won recently won for the same reason: it contained **one specific,
falsifiable technical claim** that proved he had already thought about *that client's* problem
before being paid to.

- Camera measurement, 67 applicants: *"±5mm isn't achievable camera-only. RoomPlan gets 1-3cm
  with the LiDAR you excluded. Monocular VIO studies report RMSE 1.0-1.3cm."* → **won.**
- Football tracking: *"Two of your symptoms share one root cause, and it's the homography, not the
  detector."* → diagnosis before hire.
- Drone house detection: *"The hard part is the same roof looking different three months later."*

Call it **the wedge.** It is the entire job of this skill. Everything else (structure, tone,
length) is hygiene. A letter with perfect hygiene and no wedge is one of forty forgettable
proposals.

**The wedge is risky on purpose.** It is a claim the client could check and find wrong. That is
exactly why it works: 37% of Upwork proposals are AI-written, and fluent AI produces confident
generalities, never a specific assertion it could be caught on. The risk *is* the signal.

---

## Step 1 — Load context

In parallel:
- Root `CLAUDE.md`, `Danish/CLAUDE.md`
- `references/hook-and-cta-guide.md` — hooks and CTAs
- `references/winning-patterns.md` — **read this every run.** The wedge taxonomy and worked examples
- `.claude/skills/proposal/references/cover-letter-guide.md` (repo root)
- Every `Danish/projects/*.md` in the job's domain

Pull the post if not saved: `find_jobs action=get params={job_id: "<id>"}`

---

## Step 2 — Find the wedge (do this BEFORE writing anything)

Read the post twice. On the second pass, hunt for one of these:

| Wedge type | Look for | Example |
|---|---|---|
| **The impossible spec** | A stated accuracy, latency, or cost target that published results say is unreachable | ±5mm room measurement, no LiDAR |
| **The misdiagnosis** | Client lists symptoms and implies one cause; you can see two, or a different one | "lost players" is detection dropout, "wrong ID" is no appearance model |
| **The unstated failure mode** | The thing that breaks in month three that they haven't hit yet | Seasonal roof colour drift, walls that bow, camera pan breaking a one-time homography |
| **The wrong tool** | They named a stack that will fight them | SegFormer for thin structures with a few hundred images |
| **The buried real project** | Five bullets, four routine, one genuinely hard | The one nobody else will notice |
| **The scope trap** | Budget and scope are incompatible and saying so is the differentiator | $500 fixed for 200k-image annotation plus deployment |

**When the post offers more than one wedge, lead with the type that has earned replies**
(added 2026-09-14). Read `../job-scout/references/learned-weights.json` → `current.wedge_preference`
and open on the highest-ranked type the post genuinely supports; use a second one as support if it
fits. That ranking is written only by `outcome-learner`, and only moves after 30+ judged proposals,
so until then it is the baseline order above. **Never invent a wedge to match the preference.** A
post with no wedge stays `NO WEDGE FOUND`.

Record the type in `wedge.md` as exactly one of `impossible_spec`, `misdiagnosis`,
`unstated_failure`, `wrong_tool`, `buried_real_project`, `scope_trap`, `none`. The validator copies
it into the outcome dataset; a free-text type cannot be learned from.

**Then research it.** This is mandatory when the wedge is a factual claim.

```
WebSearch: "<technique> accuracy benchmark 2026", "<framework> limitations",
           "<sensor/method> published RMSE", "<library> vs <library> <task>"
```

Bring back a real number, a real published result, or a real named limitation. `±0.4mm against
caliper ground truth` and `RoomPlan 1-3cm with LiDAR` are wedges. `high accuracy` is not.

**Research does not only verify the wedge, it upgrades it.** Go in with a hypothesis and let the
sources sharpen it. On the SDXL job the starting claim was "inconsistency is a dataset problem";
the search surfaced that removing the regularization set can *improve* fidelity and style
alignment, which is contrarian to standard advice and gave the letter a second, stronger edge.
If the research returns exactly what you assumed, you probably did not search hard enough.

**When the wedge rests on a computable number, compute it YOURSELF first, then check the
literature.** Not the other way round. On the geospatial job the arithmetic was run in `awk`
before searching — 100 km² at 30cm GSD is 1.11 gigapixels and a 3m shelter is 6 pixels at 50cm —
and the published figure then independently matched. That order matters for two reasons: an
independently derived number is one you can defend in a call, and if your arithmetic and the
literature *disagree*, that gap is itself a finding worth investigating before it reaches a client.

**Read the primary source, not a fetch summary (added 2026-10-05, ADA takeoff job).** `WebFetch` on a
PDF returned "binary content, unreadable" for Caltrans DIB 82-06, but the tool saves the file
locally and prints the path. Extract it with `pypdf` through Bash, grep the passages (the "Case"
text, the table) and quote from that. A summarising model cannot be trusted for numbers; an
extracted page can. That is how "63 in for a 4 in curb face, 126 for 8" and "Case A, B and C in
Standard Plan A88A" were verified before they reached a letter.

**If you cannot find a wedge, say so in the output.** A job with no wedge available is a lottery
ticket, and Hashim should know he is buying a ticket rather than making a bet. Write the letter
anyway, but flag it: `NO WEDGE FOUND — this is a credentials-only letter, expect low conversion.`

---

## Step 3 — Positioning and length

**Mode** — from `Danish/CLAUDE.md`. Default **engineer**: IC framing, "I built", technical metrics
only. Hard avoid: "my team", "MiniByte", "as a founder", "my company", "we", any revenue figure.
Use **founder** only when the client is buying a partner, not a pair of hands.

| Depth | Match | Mode | Words |
|---|---|---|---|
| HIGH/MED | >70% | Portfolio-led | 180-240 |
| HIGH/MED | <40% | Approach-led | 160-220 |
| HIGH/MED | 40-70% | Hybrid | 160-220 |
| LOW | any | Guide-led | 120-170 |

Shorter than the older 200-300 targets. Every approved letter landed 160-215; two came back as
too long. When in doubt, cut.

**Embedded screening questions widen the band by ~15%** (added 2026-09-14, Vision AI/CCTV job).
When the post lists screening questions in the body with no separate API field, every one must be
answered inside the letter itself — that is real, necessary content, not padding. Budget for it:
treat the table above as the base and allow up to +15% over the top of the band before treating
length as a hygiene problem. A letter that is still over even with that allowance gets trimmed for
real, not because the base band didn't account for the questions it was required to answer.

**Post-mandated sections widen the band further (added 2026-10-01, LPG cylinder and CAN gateway jobs).** When the post says "include X, Y, Z in your application" (projects, architecture, timeline, cost breakdown, availability, budget) and there is no separate field, those sections are required content. Measure the rest of the letter against the band and cap the whole letter near 330 words. Both drafts landed at 300-380 against a 160-220 band, and the 380 stood only because Hashim asked for the extra bullets. Trim the weakest bullet first, then price line items. Never trim the wedge.

**Fixed-price jobs: the price in the letter is the posted budget (added 2026-10-01).** `rate-and-boost.md` says bid the stated budget on fixed jobs. The LPG draft quoted $12,500 against a posted $15,000 and only the validator caught it. Any cost breakdown in the letter sums to the posted budget unless Hashim sets a different number. Scope the work to the budget; do not undercut it.

---

## Step 4 — Match projects honestly

- **>70%** — name it, lead with it, cite its real metric
- **40-70%** — name it as transferable. Never "I've built this exact thing"
- **<40%** — do not mention it at all

Every metric must exist in the project file. Uma machine-scores the text against the client's
stated requirements, so a stretched claim is now checkable. If a project has no quotable number,
describe what it does without inventing one.

**Proof Hashim supplies from outside `projects/` (added 2026-09-30, retail checkout job, Roomi PDF).** He may hand over a document (proposal PDF, report) and ask for it in the referenced work. Use it, but: (1) write its path into `wedge.md` so the validator can check the letter against that document; (2) if the document is a proposal or design and not a shipped system, the bullet must say so ("design for...", "scoped..."), never "built" or "live"; (3) take only facts the document states; (4) the document may say "we" or name Minibyte, and neither may leak into the letter in engineer mode. Also record the **file-verified match %** in `wedge.md`; when it differs from the scout's figure by more than 10 points (80% scout vs 65-70% checked against files on that job), say so in the hand-off to Hashim.

**Check active contracts, not only `projects/` (added 2026-09-21, depth-camera measurement job).**
Current Upwork contracts are often the most relevant proof and have no `projects/*.md` file until
someone writes one. Run `list_contracts action=search contract_statuses=["ACTIVE"]` and scan titles
for the job's domain. On the depth-camera job the letter cited AATMS and Newman Bands and missed the
live "Computer Vision/AI Engineer for Camera Measurement" contract; Hashim had to ask for it. Cite an
active contract in present tense, from its scope documents only, never with results that don't exist
yet, and never name the client.

**Scale claims need provenance (added 2026-10-01).** A project file is a draft written by us, not proof. Smart Hail Guard's "5,000 devices deployed across the US" sat in its project file, CLAUDE.md, the rubric, the validator's own examples and the embedded CV, went into about a dozen submitted proposals, and was false. Any claim of deployed devices, users, customers, revenue, "fleet", "production units" or "commercially deployed" needs a second source (an Upwork contract, client confirmation) or Hashim's confirmation recorded in the project file as CONFIRMED. If unsure, cite what was built, not the scale it reached.

**Smart Hail Guard hard rule (Hashim, 2026-10-01).** Never claim 5,000 devices, any device count, "deployed across the US", "production units", "fleet" or "running unattended" for Smart Hail Guard. It never happened. Cite it only as a hail-detection pipeline Danish built (hail vs rain and windblown debris, PyTorch/OpenCV, custom firmware, MQTT). Applies to letters, screening answers and approach docs. The old project file said otherwise; it was wrong.

**Vocabulary leak trap (caught 2026-09-08, AI Solutions Architect job):** when the letter also has
a "how I'd approach this" paragraph naming techniques for the *client's* problem, don't let that
paragraph's vocabulary bleed into a proof bullet about *past* work. The letter recommended
"per-agent token budgets" as the design approach for this client, then the StackFuse bullet said
StackFuse used "per-agent token budget allocation" — StackFuse's actual mechanism (per
`stackfuse.md`) is budget allocation between chat history and retrieved context in one shared
context layer, not a per-agent split. Caught at Gate 1, fixed before submit. Check each proof
bullet against its project file in isolation, not against the surrounding paragraph's vocabulary.

---

## Step 5 — Structure

1. **Hook** — the wedge, stated plainly. 1-2 sentences.
2. **Mini plan** — how he'd actually approach it. Named techniques, real tool names. This is the
   paragraph that proves engineer, not bidder. 2-4 sentences.
3. **Referenced work** — bullets. Format below.
4. **CTA** — binary choice plus a concrete first-mile offer. 1-2 sentences.

Understanding gets folded into the hook. Four parts, not five.

### Referenced work — bullets (supersedes the old "no bullets" rule)

```
Relevant work:
- SN3: production NLP layer, LangGraph state machine doing intent classification across eight categories with RAG over pgvector, live now.
- Anna: annotation platform where the model suggests a label and a human approves it before it counts, the verification discipline legal review needs.
```

- Two or three by default. Up to five when the post has several distinct requirement axes (edge hardware, look-alike discrimination, operator UI, audit trail) and each bullet maps to a different one (revised 2026-10-01 - was "never four"; Hashim asked for a fourth on the retail checkout job and five on the LPG cylinder job, so the cap moves, with each bullet still tied to this client).
- `Name: what it is, the technical detail that matters *here*, the real number.`
- The clause after the metric must tie to **this** client's problem. A bullet that fits any
  proposal is dead weight.
- Plain hyphens. No bold, no nesting, no emoji.

---

## Step 6 — Voice

Danish is a senior engineer in Rawalpindi messaging a peer.

**Do:** contractions everywhere. Hard variation in sentence length, a four-word sentence beside a
twenty-five-word one. Direct opinions ("I wouldn't use SegFormer here"). Comfortable admission of
limits ("I haven't done X specifically, here's the closest thing I have"). Peer shorthand
("BoT-SORT with appearance gating", not "an advanced multi-object tracking algorithm").

**Never:** em dashes (zero, not one). "I'm excited about". "Perfect fit". Rule-of-three rhetoric.
"The real question isn't X, it's Y". Mic-drop endings on every paragraph. Three paragraphs of
identical shape. AI vocabulary: delve, leverage, seamless, robust-as-filler, landscape, testament,
underscore, showcase, pivotal, crucial, tapestry.

**The Pakistan test:** would this sentence fit on a SaaS landing page? Then rewrite it.

---

**Plain language for the client (added 2026-10-01, LPG cylinder job).** Hashim rejected "floor marks give a ground-plane homography ... size comes from metric height, not pixels" with "couldn't understand this" and asked why a cashier in the loop justified a vision system. Write the plan paragraph in the client's terms: what the system does for them and when a human steps in, in words an operator, not an engineer, would use. Keep the technique names (homography, TensorRT) for the approach doc or for clients who used those words first. If the design has a human-in-the-loop step, say why the automation still pays for itself (fewer keystrokes, exceptions only, a measurable override rate) before the client has to ask.

**"No disclaimer" instructions (added 2026-09-25, DJI Matrice job).** When Hashim says to drop a
gap line and write with full authority, drop the disclaimer but still never claim the missing
experience. Put the authority in verified facts about the client's platform (researched and cited
in `wedge.md`) and in what Danish *will* do. On the DJI job the letter stated DJI's actual Matrice 4
workflow (patched MMYOLO, .pth plus per-class calibration images, DJI-side quantization) and never
said "I've deployed on DJI before". Record the gap in `wedge.md` so the validator and Hashim still see it.

## Step 7 — Format (absolute)

- Plain text. No markdown headers, bold, italics. Hyphen bullets for the project list only.
- **No hard wrapping.** Unbroken paragraph lines — hard wraps force manual reflow on paste.
- Blank line between paragraphs.
- Client's name if visible in the post.
- Mirror the client's exact stack terms and problem wording. Uma matches on it; so does the human.
- **No contact info anywhere.** Email, phone, WhatsApp, site, socials. Upwork's disintermediation
  policy prohibits it pre-contract and enforcement lands on the freelancer.
- Sign `Danish Ashraf`. Name only.
- If the post asks questions with no separate field, answer all of them inside the letter.
- **Screening field text can differ from the body text** (added 2026-09-14, Aethera). The body's
  "Please reply with" Q2 asked for the system, how you'd know it works, and the mistakes; the
  screening field version only asked for the mistakes. Answer the **fuller** version of each
  question. The validator caught the missing half on loop 1.
- **Name every source in the text** (added 2026-09-14). "A CBT study found" is vague attribution
  and failed Gate 2b three times in one letter. Write the paper's title or the benchmark name.
- **Quote a published number with its stated conditions, and use the project file's own wording**
  (added 2026-10-05, ADA takeoff job). Caltrans' 63-inch Case A run holds for an 8.3% running slope
  on a 2% cross-slope sidewalk and the first draft dropped that; the Well Log bullet said "scanned"
  where the file says "raster". Both only surfaced at Gate 1. Hedge convention claims you cannot
  cite ("usually only gives through spot elevations"), and give the client's own terms ("computer
  vision", "working demonstration") where the draft used a synonym.
- **Shared-cause claims: say "most of" or "several", not "are one gap"** (added 2026-09-14). Second
  time the single-cause trap fired (football v1, then Aethera's "problems 1, 2 and 4 are one gap").
  Name the shared piece without claiming it explains every symptom.
- **Intermediary posts: the poster is not the end client (added 2026-09-29).** "for a law firm client" means the
  poster is a developer or agency and the attorneys belong to a third party. The first draft said "your
  attorneys' worked cases" and the validator caught it. Refer to the end client as "the firm" or "your
  client", and check every "your X" against who actually owns X.
- **Never hardcode the bid in a screening answer before the liveness re-check** (added 2026-09-14).
  Aethera's Q3 said $65; the field average moved $34 -> $45 before submit and rule 2b set $55. Write
  `<RATE>` in the draft and let the validator fill it at Step 6c.
- **Availability/exclusivity questions: pull the real contract count before answering** (added
  2026-09-15, Senior Full-Stack AI-Native job). When a post asks about current commitments or wants
  someone "not juggling several other contracts," call `list_contracts action=search
  contract_statuses=["ACTIVE"]` first. Danish routinely has 5-6 active Upwork contracts running.
  Disclose that other work exists — never imply zero — but do not invent a specific hours/week
  figure the API doesn't give you either; "a couple of small, async contracts" is honest framing,
  not a fabricated number. Confirmed via research (upwork.com/blog, Sept 2026): availability is a
  live Uma ranking signal on its own, separate from the proposal text, so a vague non-answer here
  costs real ranking the same way a vague rate answer does. Flag the tension in `wedge.md` either
  way so the validator and Hashim both see it as a real fit risk, not a hidden one.

---

## Step 8 — Approach doc (restored 2026-09-16 — do not skip again)

**Build one whenever the job is HIGH technical depth, or MEDIUM with a named stack.** Root
`CLAUDE.md` has required this since the beginning; this pipeline never carried the rule forward
and silently stopped producing them.

### Why this is back

Audit of all 18 submitted proposals, 2026-09-16:

```
2026-09-01-cv-camera-measurement-room-scan   approach-doc.pdf + CV   → HIRED (contract live Sep 9)
2026-09-03-joe-lwd-measurement-arkit         3 PDFs                  → same client, follow-on work
...every other proposal folder, all 20       0 PDFs                  → 0 hires
```

One hire in the whole ledger, and it is the one job that went out with an approach doc. n=1, so
this is not proof that the doc caused the hire — but it is the only differentiated artifact in
the set, root `CLAUDE.md` puts targeted attachments at roughly +35% reply rate, and "50 people
send cover letters, maybe 2 send a technical approach doc" is the stated differentiation
strategy. Producing zero of them for six weeks was a silent regression, not a decision.

### What it is not

**It is not a ranking input.** Uma scores the cover letter and the screening answers; attachments
are not documented as reaching the shortlist stage. So the doc never carries a claim that needs
to count at ranking time — every load-bearing claim still lives in the letter and the screening
answers. The doc's job is to win the human read *after* the shortlist.

### ⚠ The PDF cannot be attached autonomously — verified 2026-09-16

`manage_proposals create` takes `attachments` as `file_uid` values, and the only way to mint a
`file_uid` is `start_attachment_upload`, which **opens an upload session for a human** and
returns a `fallback_url`. Its own contract says: *"Never ask for base64 text or local file
paths."* There is no path from a locally generated `approach-doc.pdf` to a submitted proposal
without Hashim touching an upload UI.

Hashim reviews every letter before submit (hard rule, revised 2026-09-21), so he is always in
the loop and the upload can be offered during that review. The doc still gets built —
it is what makes the letter sharp, and it is ready the moment a client replies — but at submit
time the validator reports it as available, not attached:

```
DOC       approach-doc.pdf built (4pp). Not attached — upload needs your hand.
          Say the word and I'll open an upload session before the next one.
```

Send it in the message thread once the client replies. That is autonomous and costs nothing.

**But "send it later" is weaker than it sounds (added 2026-09-18, Audio Processing Service).**
Freelancers cannot open a proposal thread — the MCP's own `manage_proposals` contract says so under
PROPOSAL MESSAGING. So a doc held back after submit reaches the client **only if they reply first**,
which is the exact thing the doc was meant to cause. There is also no way to attach it afterwards;
a submitted proposal cannot be edited.

Therefore: **offer the upload session during Hashim's review, BEFORE the submit call, not
after.** Two minutes of his time is the difference between the doc arriving with the proposal and
the doc being hostage to a reply that may never come.

### The part that IS autonomous, and was never used

`manage_proposals create` also accepts **`portfolio_project_ids`** and `certificate_ids`, which
take plain ids from `get_profile action=list_highlights` and need no upload and no human. The
pipeline has passed neither on any of the 18 proposals.

Danish has 10 attachable portfolio projects live on the profile:

```
2004143829449625600  AI-Assisted Data Annotation Platform (SaaS)
2004134768072495104  Advanced Computer Vision & Deep Learning Systems
2003805355783475200  AI-Powered Autonomous Agricultural Robot (UGV)
1757134909834051584  Object detection with satellite Imagery
1988235081997873152  AI-Powered Business Matchmaking Platform
1757150913536462848  Agriculture Boost
1988232653182840832  Custom Enterprise Conversational AI
1757148321481756672  3D modeling
1988230570776457216  Voice Automation Platform
1757146018121039872  Multi-Spectral Imaging
```

(certificates list is empty — nothing to attach there.)

**Pick 1-3 that match the projects the letter actually cites** and record the ids in `wedge.md`
so the validator passes them at submit. Re-pull the list rather than trusting these ids blindly
if a run is far from 2026-09-16 — the profile changes.

### Build it

Source of truth for the content is `wedge.md`. The doc is the wedge, expanded — not a capability
brochure.

1. Write `approach-doc.md` in the proposal folder. Structure: the problem as they stated it →
   the thing they have not accounted for (the wedge) → how you would actually build it →
   architecture or flow diagram → what you would measure → what you would deliberately not do
   in v1.
2. Render with the kit at `Upwork-Claude-Skill/generate-doc-kit` (MiniByte LaTeX template).
   Produces `approach-doc.tex` then `approach-doc.pdf`, matching the hired proposal's layout.
   **Engineer mode: the template hardcodes "MiniByte" on the cover and in the running header** (added 2026-09-30, retail checkout job; the first PDF shipped with MiniByte branding, which engineer mode forbids). Do not edit the shared kit. Copy `minibyte-preamble.tex` into the proposal folder as `engineer-preamble.tex`, replace the two `MiniByte` strings (`\small MiniByte` and `{MiniByte};`) with `Danish Ashraf`, and `\input{engineer-preamble}` instead. Read page 1 of the PDF before calling it done.
3. **Compile with the Bash tool, never PowerShell.** MiKTeX refuses to run elevated; `pdflatex`
   through Bash works. This is a known, already-paid-for lesson.
4. Max 5 pages. Include the architecture diagram (TikZ). Name and branding per the positioning
   mode selected in Step 3.

Attach the matching CV alongside it, per `Danish/CLAUDE.md` `## CV Selection` —
`cv-fullstack-ai.pdf` for SaaS/AI/fullstack, `cv-embedded-ai-ml.pdf` for embedded/robotics.

### When to skip

LOW technical depth, or a fixed budget under ~$500 where the doc costs more than the job pays.
**Skipping is a decision that gets written down**: put one line in `wedge.md` saying why. The
validator reads it and will not let an unexplained absence through on a HIGH-depth job.

---

## Step 9 — Save and hand off

Write to `Danish/proposals/YYYY-MM-DD-<slug>/`:
- `job-post.txt` — post plus every metric pulled
- `cover-letter.txt` — the letter
- `wedge.md` — the wedge, the research backing it, and the source. **The validator checks this.**
- `screening-answers.txt` — when the job has a screening field
- `approach-doc.pdf` (+ `.md`, `.tex`) — per Step 8, or the written skip reason in `wedge.md`

`wedge.md` must end with a `PORTFOLIO IDS:` line carrying the 1-3 chosen
`portfolio_project_ids` and which cited project each one backs. The validator submits them.

**Write these with the Write tool, not a Bash heredoc** (added 2026-09-14). A heredoc holding a
letter full of apostrophes failed to parse in this harness and cost a round trip.

Display the letter, then **invoke `proposal-validator`**, which owns approval and submission.

**Hashim reviews every letter before it goes out, and nothing is submitted without his explicit
approval** (hard rule, revised 2026-09-21 — was: "Hashim does not read the letter before it goes
out"). Still write it as if nobody will catch a weak wedge: his review is for his judgment, not for
fixing drafts. Max two rewrite loops from the validator, then it escalates to Hashim.

**Non-standard submission formats do not exempt this flow (added 2026-09-14, Principal AI-Native
Architect job).** A job post that says "we'll send a technical questionnaire instead of a cover
letter," or otherwise implies the normal proposal text doesn't matter, still requires: the
`Danish/proposals/YYYY-MM-DD-<slug>/` folder, the Step 2 wedge search, and a `proposal-validator`
invocation before submission. Upwork's `cover_letter` field is still required by the API and is
still the only text a human or Uma reads before any questionnaire exists — write it with the same
rigor and pass it through the validator like any other job. What changes is only the CTA (state
readiness for their process instead of forcing the standard binary call/2-slide-deck choice), not
the workflow. On the job above, the letter was hand-drafted directly in conversation with Hashim
reviewing and editing it live — skipping this entire skill and proposal-validator's Gates 0-4.
That skipped the wedge search and Gates 0-4, and happened only because the unusual format didn't
visibly trigger the normal chain. It worked out (claims were
manually double-checked against `projects/hoki.md` before submission), but treat any job with an
atypical proposal mechanic as a prompt to explicitly invoke this skill and the validator, not a
reason to freelance the letter in the main conversation.
