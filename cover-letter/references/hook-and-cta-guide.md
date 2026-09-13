# Hooks and CTAs — the two sentences that decide everything

85% of clients read the first paragraph and stop. The hook is the whole letter's job interview.
The CTA is what turns a nod into a reply.

---

## Part 1: The hook

### What we're aiming for

**Spicy but soft.** Those aren't in tension, they're the whole trick.

- **Spicy** = you have an actual opinion about their problem. You noticed something. You're not
  reciting their post back at them.
- **Soft** = you're not correcting them, not showing off, not selling. You're a peer who read
  the thing and had a thought.

The feeling a good hook produces in the client is *"oh, this person already gets it"* — not
*"wow, impressive"* and definitely not *"this guy thinks I'm stupid."*

### The one rule

**Write every hook from scratch.** Templates are the number one tell that a proposal is
AI-generated, and clients in 2026 are pattern-matched to death. If your opening could survive a
find-and-replace into a different job post, it's dead.

### How to find the hook

1. Read the post twice. The second time, look for the sentence where the client is quietly
   describing something that's harder than they think it is.
2. That's your hook. Name it, plainly, and show you know why it's hard.
3. Don't solve it in the hook. Just prove you see it.

The client wrote five bullet points. Four are routine. One is the real project. Open on that one.

### Hooks that worked (real, from approved letters)

> "Two of the symptoms you listed share one root cause, and neither needs a rebuild."

*Why it works:* immediately reframes their five-bullet problem list into something structured,
and the "neither needs a rebuild" defuses their obvious fear (that this is a big expensive job)
in six words. Soft, because it's reassuring, not corrective.

> "The hard part here isn't detecting a house in one clean shot, it's keeping the detections
> stable when the same roof looks different three months later because the paint faded, the trees
> grew, or the light changed."

*Why it works:* concrete, physical, specific to *their* imagery. Names a failure mode they will
absolutely recognise from their own data. Nobody else bidding will mention seasonal drift.

> "Replacing hardcoded scoring is the easy part. The real bar is reliability: the same document
> scoring the same every time, and every classification defensible if someone asks why."

*Why it works:* takes the client's stated task and identifies the standard they'll actually be
judged against. Two short sentences, no hedging.

> "Your ±5mm target is the whole project, so I'll be straight about it: that number is real for
> fixed objects and openings, and it isn't for full-room dimensions from a camera alone."

*Why it works:* the honest-no. Sixty-six other applicants said yes. This one told the truth with
a number attached, and won the job. **Highest-risk, highest-reward hook type — only use it when
you can back it with published figures.**

### Hooks that are dead on arrival

| Pattern | Why it fails |
|---|---|
| "I noticed you need X" | Robotic pattern-matching. Says nothing. |
| "Your X is like a Y" | Forced metaphor. Reads as trying too hard. |
| "[Name], I saw your post about X" | Obvious template slot. |
| "The real challenge isn't X, it's Y" | Was fresh two years ago. Now it's a tell. |
| "I'm excited about this opportunity" | Instant skip. |
| "With 7+ years of experience in..." | Nobody has ever read past this. |
| Any opening that restates their requirements | They wrote them. They know. |

### Structural variety

Track how the last few hooks opened and **do not repeat the entry point.** Rotate:
- A flat technical claim: *"Calibration drifting when the camera moves comes from the homography."*
- A reframe: *"Two of the symptoms you listed share one root cause."*
- A concession: *"Your ±5mm target isn't reachable camera-only, and here's the number."*
- A number: *"±5mm across a 4m wall is 0.125% relative error."*
- The quiet part: *"The hard part isn't X, it's what happens three months later."*

Starting with "I" three letters in a row is a pattern. Break it.

---

## Part 2: The CTA

### Shape

**Binary choice + first-mile offer.** Never open-ended. "Let me know if you're interested" is
where proposals go to die.

The client should be able to reply with one word.

### The first-mile offer is the actual engine

Give away something small, concrete, and immediately useful — before any money moves. It removes
risk, proves competence, and gets a reply from clients who weren't going to write one.

Patterns that have worked:
- *"Send me two or three sample drone images over one of your areas and I'll return annotated
  detections so you can see the accuracy before we scope the full script."*
- *"Send me one placeholder function and a few sample documents and I'll return a working version
  plus its eval before you commit the rest."*
- *"Send the screen recording and repo access and I'll come back with the confirmed root cause, a
  fixed price, and a timeline."*
- *"I'd start with a 24-hour audit of your current setup. No charge, you keep the findings either
  way."*

Notice the shape: **you send me a small thing, I send you back a real thing.** Not "let's hop on
a call to discuss." A call is work for them. A deliverable is work for you.

### CTA rules

- One sentence, two at most.
- Ask for something small and specific ("two or three sample images", "one placeholder function").
  A vague ask ("send me your requirements") gets ignored.
- Name what they get back, concretely.
- Optional second half: the binary. *"Should I start from the recording, or a 10-minute call first?"*
- Never stack two questions. Never end with "Looking forward to hearing from you."

### On pricing in the CTA

When a client asks for a fixed price before showing you the materials, **don't quote blind.**
Saying so is a differentiator, not a dodge:

> "I won't quote a fixed price blind. Send the recording and repo access and I'll come back with
> the confirmed root cause, a fixed price, and a timeline, scoped to the smallest change that
> makes the test video run reliably."

That paragraph won a job against 66 applicants who all guessed a number.

---

## Part 3: The voice test

Read the finished letter aloud. Ask:

1. **Peer or vendor?** Does it sound like an engineer messaging another engineer, or a service
   provider pitching? Vendor language is the most common failure.
2. **Would a real person type this?** Contractions present? Sentence lengths varied? Any sentence
   that would fit on a SaaS landing page?
3. **Is every claim checkable?** Every project named, every number, every "I built" — verifiable
   in `Danish/projects/*.md`.
4. **Could this letter go to a different client?** If yes, it isn't specific enough yet.
5. **Any em dashes?** Should be zero.
6. **Silicon Valley leak?** Danish is a working engineer in Rawalpindi, not a growth-stage
   founder. "We're excited to partner with you on this journey" is a fail. "I'd start by checking
   how often the homography is recomputed" is right.

If any answer is wrong, rewrite before it goes to validation.
