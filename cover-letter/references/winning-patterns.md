# Winning patterns — the wedge taxonomy

Post-mortems of what actually converted, and why. Read before writing.

---

## Why the wedge works

Upwork in 2026: Uma Recruiter machine-ranks proposal text against the client's stated
requirements and hands the client a shortlist within ~6 hours. 37% of proposals are AI-written.
The client reads maybe six.

Every proposal in that pile says some version of *"I have N years of experience and I can do
this."* Fluent, competent, interchangeable. LLMs are extremely good at producing it, which is
exactly why it no longer signals anything.

**What no generic proposal contains is a specific claim about the client's problem that could be
wrong.** Making one requires having actually thought about their situation. It is expensive to
fake and cheap to verify, which makes it the only reliable signal left.

That is the wedge. It is the whole strategy.

---

## The six wedge types

### 1. The impossible spec

The client has named a target that published results say is unreachable. Say so, with numbers,
and offer the reachable version.

**Camera measurement, 67 applicants, WON:**
> "Your ±5mm target is the whole project, so I'll be straight about it: that number is real for
> fixed objects and openings, and it isn't for full-room dimensions from a camera alone. Apple's
> RoomPlan lands within 1-3cm, and that's with the LiDAR you've ruled out. Published monocular VIO
> studies report RMSE around 1.0-1.3cm."

Why it won: 66 people said yes to an impossible number. One said no and showed the arithmetic.
The client hired the one who told the truth, because that is the person who will not blow the
budget discovering it in month four.

**Requirements:** you need real published figures. Research before claiming. Then always offer the
tiered achievable version, otherwise it reads as a refusal rather than expertise.

### 2. The misdiagnosis

The client lists symptoms and implies one cause. You can see it is two, or a different one.

**Football tracking:**
> "The problems you listed split into two separate causes, and neither needs a rebuild. Calibration
> drifting when the camera moves comes from the homography [...] Lost and unstable tracking is a
> second, separate issue: players get missed when the detector's confidence drops under occlusion."

Why it works: diagnosis before being hired is the single most expensive thing to fake. It also
quietly proves you read all five bullets, not just the title.

**Trap:** do not collapse distinct symptoms into one root cause because it reads cleaner. If the
client listed detection dropouts *and* ID switches, those are two problems. Collapsing them
under-covers the post and a technical client will notice.

### 3. The unstated failure mode

Name the thing that breaks in month three that they have not hit yet.

**Drone house detection:**
> "The hard part here isn't detecting a house in one clean shot, it's keeping the detections stable
> when the same roof looks different three months later because the paint faded, the trees grew, or
> the light changed."

Why it works: they will recognise it from their own data instantly, and nobody else bidding will
raise it. It reframes a commodity task (object detection) as a specialist one (change robustness),
which also justifies a higher rate.

### 4. The wrong tool

They named a stack that will fight them. Recommend against it, with the reason.

**Roofline segmentation:**
> "I'd use a compact U-Net with a pretrained MobileNet or EfficientNet-B0 encoder rather than
> SegFormer-B0. Rooflines are thin, high-frequency structures and the output is going straight
> into a polyline, so boundary precision from the skip connections matters more here than a
> transformer's global context."

Why it works: the client explicitly invited a recommendation ("your call, tell me why"). Taking a
side with a stated reason is the answer; hedging is not.

**Trap:** only when you can defend it technically. Contrarianism without a reason is worse than
agreeing.

### 5. The buried real project

Five bullets, four routine, one genuinely hard. Open on the hard one.

**Legal-tech NLP:**
> "Replacing hardcoded scoring is the easy part. The real bar is reliability: the same document
> scoring the same every time, and every classification defensible if someone asks why."

Why it works: the client wrote the task. You named the standard they will actually be judged
against. That is the difference between a contractor and an engineer.

### 6. The scope trap

Budget and scope are incompatible, and saying so is the differentiator.

> "I won't quote a fixed price blind. Send the recording and repo access and I'll come back with
> the confirmed root cause, a fixed price, and a timeline, scoped to the smallest change that makes
> the test video run reliably."

Why it works: every other bidder guessed a number. Refusing to guess, then offering a concrete
path to a real number, reads as the only professional in the pile.

---

## The first-mile offer

The wedge earns attention. The first-mile offer converts it into a reply.

Shape: **you send me a small specific thing, I send you back a real thing.**

- "Send me two or three sample drone images over one of your areas and I'll return annotated detections."
- "Send me one placeholder function and a few sample documents and I'll return a working version plus its eval."
- "Send the screen recording and repo access and I'll come back with the confirmed root cause, a fixed price, and a timeline."

Not "let's hop on a call." A call is work for them. A deliverable is work for you. Asking for
something small and specific ("two or three images") converts far better than "send me your
requirements."

---

## Calibration: what does NOT win

| Pattern | Why it fails |
|---|---|
| Credentials-first ("7+ years, Top Rated Plus") | Everyone has credentials. Zero information. |
| Restating their requirements back | They wrote them. |
| Generic method lists ("YOLO, OpenCV, PyTorch") | Names of tools ≠ judgment about tools. |
| Enthusiasm ("excited to work on this!") | Instant skip. |
| Portfolio link dump | Client stops at the first one. |
| Forced project match | A technical client spots it, and it costs credibility on every other claim. |
| Hedged everything ("we could explore several approaches") | Reads as having no opinion, which reads as no experience. |

---

## When there is no wedge

Some posts genuinely offer none: three vague sentences, no stated stack, no numbers, no
contradictions. In that case:

1. Say so in the output (`NO WEDGE FOUND`), so Hashim knows the conversion odds are low.
2. Fall back to **guide-led**: interpret what they probably need, since they were vague because
   they do not know. Show domain knowledge through the interpretation, not through questions.
3. Make the first-mile offer the centre of gravity instead of the hook.
4. Keep it short. 120-150 words. There is nothing to say at length.

**Never manufacture a fake wedge.** An invented technical objection to a problem that does not
have one is worse than a plain letter, because a technical client will catch it and everything
else you claimed becomes suspect.
