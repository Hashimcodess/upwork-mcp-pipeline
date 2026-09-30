# Capability 2: portfolio creation

Runs only after a **BUILD** verdict **and** an explicit "go" from Hashim. Everything lands in
`Danish/dummy-portfolio/<slug>/`. Nothing is published, pushed or uploaded by this skill.

## B1. Abstract the brief

Write the problem in your own words, client-free:

- One paragraph: the generic problem, the input, the output, why it is hard.
- A success bar, **fixed before any code is written**: the numbers the piece will be judged on
  (for example "coverage of ground-truth roof area, edge reprojection error in px, run time").
- Strip: client name, company, product names, their dataset, their benchmark, their scoring
  harness, and any sentence lifted from the post. The post's id and URL live only in the private
  validation scorecard.

## B2. Choose the format, slug and effort cap

| Format | Use when | Provenance line |
|---|---|---|
| **Reference implementation** | The problem is a build | "Reference implementation built to demonstrate <approach>. Not delivered client work." |
| **Benchmark study** | The value is a comparison of methods | "Independent benchmark of <methods> on <dataset>. Methodology and results below." |
| **Synthetic-data study** | No public data fits, but honest generation does | "Study on synthetic data generated with <generator>. Not real-world results." |

`slug` is short kebab-case, named for the problem class, never the client.
**Effort cap: default 3 working days.** Ask Hashim to confirm or change it. If the honest scope
does not fit the cap, cut scope and say what was cut. Do not stretch the cap silently.

## B3. Plan, then stop for approval

Write `plan.md` and show it:

- Success bar, dataset(s) with **name, version and licence**. The licence must allow portfolio
  display. **Read the dataset's own licence and access terms (its download page, its Hugging Face
  card, its gating prompt), never the upstream source's.** A processed or annotated redistribution
  can be far stricter than the raw data underneath it (Building3D is CC BY-NC-SA 4.0 and gated,
  while the Estonian Land Board data beneath it is open). Never accept a licence, gate or
  data-use agreement on Hashim's behalf. Record the licence in `metrics.md`, models and libraries, hardware, expected run time.
- What the finished piece will show, and the 3-5 assets that will show it.
- **Where the demo will live.** Hashim has not chosen a host. Options: a local folder ready to
  push to a public GitHub repo, or a hosted demo (Hugging Face Spaces and similar would need a
  connector). Ask, name the specific connector you would need, and do not work around it with
  something weaker. Default: local folder, nothing pushed.
- Anything that needs a resource not available (GPU, dataset download, screen recorder):
  say so now.

Wait for a yes. No code before it.

## B4. Build

`code/` is runnable: pinned requirements, a single command to reproduce the headline numbers,
no secrets, no absolute local paths.

**Numbers are measured or absent.**

- Run it, on the stated hardware, on the stated data. Record the command, the seed, the date.
- Report misses honestly. A method that reaches 78% against a 90% target is a legitimate,
  credible result. An invented 91% is not, and is the fastest way to lose a technical buyer.
- Include failure cases: three or four worst outputs and why they fail. Technical clients read
  these first.
- If a claim cannot be measured, delete the claim.

## B5. Assets

| Asset | Notes |
|---|---|
| Architecture / pipeline diagram | The Figma MCP `generate_diagram` makes a clean one, but it creates real files in Hashim's connected Figma account, so say so and ask first. Otherwise render locally (Mermaid or matplotlib) |
| Results figure | One image that shows the headline result at a glance. Charts follow the `dataviz` skill if available |
| Demo clip / GIF | `ffmpeg -version` to check availability. If a clip needs a recorder or a hosted demo, ask |
| Failure-case panel | The worst outputs, labelled |

## B6. Deliverables

```
dummy-portfolio/<slug>/
  README.md        provenance line first, what it is, what it proves, how to run
  metrics.md       measured numbers, hardware, dataset + licence, protocol, seed, date, failure cases
  upwork-copy.md   paste-ready portfolio entry (below)
  plan.md          the approved plan
  assets/          diagram, results figure, GIF, failure panel
  code/            runnable, pinned, one-command repro
```

**`upwork-copy.md`** is what Hashim pastes into Upwork:

```
TITLE        <= 70 characters, front-loaded with the terms clients search on
ROLE         <role, honest>
DESCRIPTION  Line 1 is the provenance line, verbatim. Then: the problem, the approach, the
             measured result with its dataset, one honest limitation.
             Write a SHORT version (about 600 characters) and a LONG version. Upwork's form
             limits change, so check the current limit in the form before pasting.
SKILLS       Names that exist in Upwork's skill list, taken from the client wording in the
             validation. Unmatched names are rejected by Upwork, never guessed.
LINKS        Repo or demo URL, only if Hashim has published one.
ATTACHMENTS  Which files from assets/ to upload, in order.
```

## B7. Honesty line

| Legitimate | Not legitimate |
|---|---|
| A demo, benchmark or reference build labelled as one | Presenting it as delivered client work |
| Real numbers measured on the piece itself | Numbers taken from a paper or a client's post as if you produced them |
| A public dataset, named and licensed | The client's data, schema, benchmark or scorer |
| "Built to demonstrate" | "Built for", "delivered to", or any client, logo or testimonial |
| Limitations and failure cases stated | Invented outcomes ("cut costs 40%") from a system nobody ran |

Upwork can remove a profile for misrepresentation, and one invented metric makes a technical
buyer discount the whole page. Danish's standing is worth more than any single piece.

## B8. Final check, then hand over

Before saying done:

1. **Re-run** the reproduction command once and confirm the numbers in `metrics.md` match.
2. **Trace every claim** in `README.md` and `upwork-copy.md` to a line in `metrics.md`.
3. **Residue check.** `Grep` the deliverables for the client's name, the job id, and 3-4
   distinctive phrases from the original post. Any hit is removed.
4. **Provenance line** present, first, and verbatim in both README and upwork-copy.
5. **Licences** recorded for every dataset and model.

Then tell Hashim plainly: **there is no Upwork API for adding an individual portfolio project**,
so he uploads it himself at Profile → Portfolio → Add project. Do not imply an automated upload is
coming. Do not touch the profile, and never call any Upwork write tool.
