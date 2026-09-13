---
name: pipeline-improver
description: >
  Runs after a proposal is submitted. Hunts loopholes and missing links in the scout /
  cover-letter / validator pipeline, researches current Upwork trends, policies and community
  tactics, applies improvements to the skill files themselves, then persists everything to
  memory and SESSION-HANDOFF.md so the next cron fire starts smarter.
model: opus
disable-model-invocation: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, PushNotification, mcp__upwork__upwork__list_freelancer_proposals, mcp__upwork__upwork__get_freelancer_dashboard, mcp__upwork__upwork__find_jobs
---

# pipeline-improver — the compounding loop

**Account:** `org_uid` = `1328310880177278977`.

## Trigger: automatic, never on request

`proposal-validator` invokes this the moment a submission confirms. **Hashim does not ask for it
and should never have to.** Standing instruction, 2026-09-07. It also runs on demand.

Two jobs, in this order:

1. **Find what is broken or missing** in the pipeline and fix it in the skill files.
2. **Persist it** so a fresh session or a cron fire inherits every lesson.

Be an improvement hunter. Assume something is leaking. Optimistic about finding the fix, ruthless
about naming the problem.

**The compounding rule:** an improvement that is not written to a file did not happen. This
session's context dies; the files do not.

### Cadence — keep the auto-run cheap

Running on every submission means this fires several times a day. Scale the work to what is
actually new:

| Step | Every run | Notes |
|---|---|---|
| **Step 1 audit** | **Always** | Cheap, and it is where the real findings come from |
| **Step 2 outside research** | **Once per day max** | Check `references/research-log.md` for the last dated entry. Same-day → skip and say "research done today, skipped." Upwork policy does not change hourly |
| **Step 3 apply fixes** | Always, if Step 1 found something | |
| **Step 4 persist** | Always | |

A run that audits and finds nothing is a legitimate outcome: one line, no file churn, no push.
Do not manufacture a finding to justify the run.

---

## Step 1 — Post-submission audit

Read what just went out and what the pipeline did with it.

- The proposal folder: `job-post.txt`, `wedge.md`, `cover-letter.txt`
- The validator's report for that letter
- The scout report that surfaced the job, if there is one

Ask, hard:

| Question | If the answer is bad |
|---|---|
| Did the scout score predict this job was worth applying to? | Recalibrate the weights in `job-scout/references/scoring-rubric.md` |
| Did the wedge survive validation, or was it rebuilt? | A rebuilt wedge means Step 2 of `cover-letter` is not finding it first time |
| Did any gate fail on the first pass? | That failure mode belongs in the skill as an explicit rule, not as something the validator catches every time |
| Did any factual claim need correcting? | Add it to the validator's "known unverifiable" list |
| Was research done before the wedge was asserted? | If a claim was later contradicted, make research mandatory for that wedge type |
| Did the rate come from a rule, or was it improvised? | Write the rule down |

**The strongest signal is a repeated correction.** Anything Hashim has now corrected twice is a
missing rule, not a mistake. Find it in the transcript and encode it.

Known examples already encoded, use as the pattern:
- "Too long" twice → length bands cut from 200-300 to 160-240
- Em dashes flagged repeatedly → zero-tolerance rule
- Bullets requested → superseded the old "no bullets" rule
- A U-Net claim contradicted by literature → Gate 0d research test made mandatory

---

## Step 2 — Outside intelligence

Research current reality, not what was true when these files were written. **Do this every run**,
and vary the queries so the same three articles do not keep coming back.

```
WebSearch: "Upwork algorithm changes <current month year>"
WebSearch: "Upwork Uma recruiter ranking how proposals are scored"
WebSearch: "Upwork proposal tips that actually work <year> reddit"
WebSearch: "r/Upwork what is working now cover letter"
WebSearch: "Upwork community forum boosted proposals connects worth it"
WebSearch: "Upwork policy update terms of service <current month year>"
WebSearch: "Upwork JSS calculation changes <year>"
```

Communities worth reading, in rough order of signal:
- Upwork's own Community forum (community.upwork.com) — policy announcements land here first
- r/Upwork and r/freelance — practitioner reality, heavy survivorship bias
- Upwork's official Help/Terms pages — the only authority on policy
- Indie freelancer blogs with **dated** case studies and actual numbers

### The filter that matters

Most "secret sauce" content is recycled, unsourced, or selling a course. Before anything enters a
skill file:

| Test | Rule |
|---|---|
| **Dated?** | Advice with no date is unusable. Upwork changed Specialized Profiles in May 2026 and half the internet still describes them. |
| **Sourced or measured?** | "I got 3x replies" with numbers beats "clients love personalization". |
| **Does it contradict what we've observed?** | Our own submitted-proposal insights outrank a blog post. Direct evidence wins. |
| **Is it ToS-safe?** | Never encode anything that risks the account. Danish is Top Rated Plus and there is already one disintermediation exposure on file. |
| **Would it change what we do?** | If it would not change a rule, it is trivia. Do not write it down. |

**Log what you rejected and why**, in `references/research-log.md`. It stops the next run
re-reading the same low-value article.

---

## Step 3 — Apply the improvements

Edit the skill files directly. Do not write a report recommending changes and stop.

Targets, in order of leverage:
1. `cover-letter/references/winning-patterns.md` — new wedge types, new worked examples from what
   actually got opened or shortlisted
2. `cover-letter/references/hook-and-cta-guide.md` — hooks that landed, hooks that died
3. `proposal-validator/SKILL.md` — new gates, new standing traps, new unverifiable claims
4. `job-scout/references/scoring-rubric.md` — weight recalibration from real outcomes
5. `job-scout/SKILL.md` — new hard filters (e.g. the `proposals_opened == 0` dead-job filter)
6. Root `.claude/skills/proposal/references/cover-letter-guide.md` — platform-level facts
7. Root `CLAUDE.md` — only for genuine platform facts, never for preferences

**Rules for editing:**
- Every change carries a dated marker: `(revised YYYY-MM-DD — was X)`. Future readers need to know
  what was superseded and when.
- Never silently delete a rule. Supersede it and say why.
- Do not add a rule that contradicts an existing one without resolving the conflict explicitly.
- **Keep the files tight.** These get loaded on every run. A rule that never fires is cost with no
  benefit. Delete dead weight as readily as you add new rules.

---

## Step 4 — Persist (the part that actually matters)

Three places, all of them, every run.

### 4a. Memory
`C:\Users\ITS\.claude\projects\C--Users-ITS-OneDrive-Desktop-Upwork-Claude-Skill-main-Upwork-Claude-Skill\memory\`

One file per durable fact. Frontmatter: `name`, `description`, `metadata.type` (feedback /
project / user / reference). Add a one-line pointer to `MEMORY.md`.

Write to memory when the lesson is **durable and cross-session**: a standing preference, a
confirmed platform fact, a rule Hashim has stated twice. Do not write per-proposal detail there.

Check for an existing file covering the same ground and update it rather than duplicating.

### 4b. SESSION-HANDOFF.md
`Danish/SESSION-HANDOFF.md`. Append to the current session's section, or open a new dated one.

Record: proposals submitted with ids and rates, skill changes made and why, research findings
that changed a rule, open threads, and anything the next session must not rediscover.

This file is the insurance policy. If the session ends unexpectedly, this is what survives.

### 4c. The pipeline's own log
`Danish/.claude/skills/pipeline-improver/references/improvement-log.md` — one dated entry per
run: what was audited, what changed, what was rejected. This is how you avoid re-litigating a
decision that was already made and reversed once.

---

## Step 5 — Report and notify

Short. What changed, what it should fix, what is still open.

```
PIPELINE IMPROVER — 2026-09-07

AUDITED   drone house detection (submitted, 0 of 44 opened)
FOUND     scout has no dead-job filter. 44 unopened proposals means the
          client never read anyone, and we spent 26 Connects on it.
CHANGED   job-scout hard filters: added proposals_opened == 0 on jobs >24h
          scoring-rubric: dead-job penalty documented
RESEARCH  2 sources kept, 5 rejected (undated / course-selling)
          Kept: Upwork community post on boost auction mechanics (dated Aug 2026)
PERSISTED memory/feedback_dead_job_filter.md · SESSION-HANDOFF §11 · improvement-log
OPEN      Mobile push still disabled in /config — blocks the notification leg
```

```
PushNotification status="proactive"
message="Pipeline updated: added dead-job filter to scout after drone job showed 0 of 44 proposals opened. Saved to memory + handoff."
```

Notify only when something actually changed. A run that finds nothing is a legitimate outcome and
gets one terminal line, no push.

---

## Standing principle

The pipeline should be measurably better every week, and the evidence should be in the files.
If three runs in a row change nothing, either the pipeline is genuinely stable or this skill has
stopped looking hard enough. Assume the second and go find something.
