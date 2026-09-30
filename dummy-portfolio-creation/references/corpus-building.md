# Building the evidence corpus

The validation only means something if it is honest about what evidence it had. This file says
how to gather it, and what the API can and cannot do. **Measured 2026-09-30**; re-probe on the
first real run and update the "Measured limits" table if anything moved.

## Measured limits

| Tool | What it gives | Depth | Caveat |
|---|---|---|---|
| `find_jobs action=search` (`query`, `sort: recency`) | Class-specific, whole marketplace | About **3 weeks**. Cursor `200` reached Sep 15, cursor `300` reached Sep 7-8, cursor `500` and `1000` returned empty. Practical ceiling is offset ~300-400 per query | No date filter. 10 rows per page. Cursor is a numeric offset string (`"10"`, `"20"`, ...) |
| `find_jobs action=smart_search`, `mode: most_recent`, `from_date` / `to_date` | Personalised feed with a **real date filter** | Reached **at least Jun 23** (~14 weeks): a Jun 22-30 window returned 3 rows. A Jun 15-21 window returned nothing, so the edge is near Jun 21 or that week had no matches | Personalised to Danish and **not filterable by topic**. Volume is high (`total_matching` was 51 for Aug 8-21, 177 for Aug 22-Sep 4, 117 for Sep 5-11) but each call returns only 10 rows, newest first, so counting one class across weeks would take 10+ pages per week. Use it to inspect what the feed held, not to count a class. **Treat every older-week count as a lower bound** |
| `find_jobs action=search` with `title` (1-3 words, sort `recency`) | Niche-term title match | A niche term **exhausts the retained index** (`hasMore: false`). Measured: title "photogrammetry" returned 3 posts spanning Aug 21, Aug 24 and Jul 27; "DSM", "orthomosaic" and "building footprint" returned 1 each | The best way to see how far back a *niche* class really goes. Broad terms drown in noise: title "roof" returned roofing-business marketing and cold-calling gigs, not engineering. Cannot be combined with `query` |
| `find_jobs action=get` | Full post, client record, hire funnel | Live jobs only | One call per job. Do not use for the sweep, only for the post being validated |
| `job-ledger.jsonl` (this skill) | Everything any run has ever seen | Grows every run | The only record that gets longer than the API allows. The 3-4 month window is reached by accumulating, not by asking |

Consequence: on the first run the honest window is roughly **3 weeks of class-specific data
plus a sparse 13-week sample**. Say so in the scorecard. Confidence rises as the ledger fills.

## The sweep (run this for every validation)

1. **Extract class terms** from the post, in the client's own wording, plus 3-5 synonyms a
   different client would use for the same problem. Also extract 2-4 `--exclude` words that
   would pull in false positives.
2. **Live sweep.** 6-10 queries, `action=search`, `sort: recency`, `limit: 10`.
   Page the two or three best queries with cursors `10, 20, ...` until `hasNextPage` is false,
   the rows are older than ~25 days, or the offset passes ~300. Take the rest to offset ~100.
   Budget about 30 calls total. Do not pass `include_full_details`; snippets are enough.
3. **Niche title sweep.** Run 4-6 `title` searches with niche 1-3 word terms from the class
   (for a roof problem: "DSM", "orthomosaic", "photogrammetry", "3D reconstruction",
   "building footprint"). Page each until `hasMore` is false. This shows the deepest history
   the index holds for the class, often several weeks further back than the recency sweep.
   Skip broad words that drown in business gigs.
4. **Dated feed (optional).** `smart_search`, `mode: most_recent`, `from_date` / `to_date`
   for a specific week you want to inspect. It cannot be filtered by topic, so it is a sample.
   Do not try to count a class through it.
5. **Record what touches the class.** Record every row that matches the class **or an adjacent
   class** (measurement or geometry from the same kind of imagery). Rows clearly unrelated
   (marketing, sales, annotation labour) can be skipped to save tokens; the ledger only
   needs the rows that can answer a demand question. Write the rows to a scratch JSON file
   and load them:
   ```
   python .claude/skills/dummy-portfolio-creation/scripts/ledger.py add --file <rows.json> --source search
   python .claude/skills/dummy-portfolio-creation/scripts/ledger.py add --file <rows.json> --source smart --now <latest API timestamp>
   ```
   Row fields: `id, title, published_date, job_type, budget, proposal_count` (or
   `proposals_tier`), `skills, description_snippet, client_key, client_spent`.
   **`client_key` = `country|round(total_spent)|total_reviews`** so a client who reposts the
   same job collapses to one buyer. Search rows carry no client id, so this fingerprint is the
   best available.
6. **Read the numbers.**
   ```
   python .claude/skills/dummy-portfolio-creation/scripts/ledger.py stats --terms "a,b,c" --exclude "x,y" --days 120
   python .claude/skills/dummy-portfolio-creation/scripts/ledger.py span
   ```
   Run `stats` once for the core term set and once for an adjacent variant so the scorecard can
   say whether the demand is narrow or broad.
7. **Clean the matches by eye.** Keyword matching is word-start (so `roof` finds `roofline` but
   not `proof`), and is still fuzzy. Read the `titles` list, drop obvious
   false positives with `--exclude`, and re-run. Never score off a count you have not sanity-read.

## Rules

- "Now" is the newest API timestamp seen in the run, never the machine clock (it runs about 12
  hours behind). The script already anchors on the newest published date in the ledger.
- One client reposting one job is **one** data point of demand, not five. Report `unique_clients`
  and treat `matches` as secondary.
- Search rows carry `total_spent` but no hire count. Use spend as the buyer-quality proxy and say
  that is what it is.
- A tier (`50+`, `20 to 50`) is not a count. When only tiers are available, report tiers, never a
  number, and do not average them.
- Older-week counts are lower bounds. Never write "demand fell" from a smaller older-week count
  alone; the trend line is only scored once the ledger span is at least 28 days.
