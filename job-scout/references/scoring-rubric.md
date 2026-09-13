# Scoring rubric — domain map and match calibration

## Scope

**Score against the whole profile and all 40 projects, not a shortlist of verticals.**
(Revised 2026-09-07.) Computer vision, drones, AI/ML and embedded are where Danish is strongest,
but the portfolio is much wider and a job in any of it is fair game at ≥40%.

Also read `Danish/profile/upwork-profiles/main-profile.md` before scoring. It carries the live
Uma-matched profile text, the `## Keywords To Mirror` list, and the **real Upwork work history**,
which outranks portfolio claims because a client can see the rating and spend:

| Contract | Value | Why it matters |
|---|---|---|
| Embedded ML model development, synthetic data tooling, Python + C | **$19,360 @ $40/hr, 484 hrs, 5.0** | Strongest single artifact. Long-running, hourly so hours are Upwork-tracked |
| CV model reading expiry/batch codes on packaging | $2,100 fixed, 5.0 | Industrial OCR/inspection |
| Distributed federated AI, NVIDIA platforms | $1,000 @ $40/hr | Federated learning |
| MLOps on Azure | $900 @ $30/hr | Cloud MLOps |
| Lead Architect, AI-powered development automation | $250 @ $50/hr, 5.0 | "Agentic Architecture was great" |
| Ostris masked-dataset LoRA training | $200 fixed, 5.0 | Diffusion fine-tuning |
| AI Voice Bot | $200 fixed, 5.0 | Voice AI |
| ROS 2 alternative framework review | $50 fixed, 5.0 | Robotics frameworks |

Standing: **Top Rated Plus, 100% JSS, $50K+ earned, 24 jobs, 1,087 hours.** Live rate $65/hr,
30+ hrs/week available, response time 0-4 hours.

## Danish's domains, mapped to project files

Match scoring is only honest if it is anchored to actual files in `Danish/projects/`.
Read the relevant ones before assigning a percentage. Never score from the project *name*.

### Computer vision — detection, tracking, segmentation
| Project | What it actually proves |
|---|---|
| `trackzella.md` | Sports analytics, player + ball tracking, NVIDIA optical flow, real-time |
| `generic-object-tracker.md` | Multi-domain tracking (aerial/ground/maritime), sliced inference for small objects in large images, TensorFlow |
| `satellite-imagery-analytics.md` | Aerial/satellite detection, ortho-map generation, chronological pre/post change comparison, defense + disaster response |
| `well-log-digitization.md` | U-Net semantic segmentation trained from scratch, YOLO detection, SVM, OCR, multi-stage pipeline. Days → under 1 hour |
| `trackue.md` | Face recognition, eye landmark detection, edge processing |
| `urban-guard.md`, `netauto.md` | Surveillance, vehicle/urban tracking |

### Drones / navigation / aerial
| Project | What it proves |
|---|---|
| `gps-denied-navigation.md` | Visual positioning from scratch, ORB/SIFT correspondence, homography, Kalman filtering, no platform tracking framework. Defense application |
| `autonomous-inspection-drone.md` | Autonomous flight + inspection |
| `fabsky.md` | Drone hardware |
| `satellite-imagery-analytics.md` | Overhead imagery analysis |

### Embedded / edge ML
| Project | What it proves |
|---|---|
| `guardio.md` | 100 FPS on Jetson Nano after TensorRT optimization |
| `smart-hail-guard.md` | 5,000+ devices deployed in the US |
| `ensemble-smart-lighting.md`, `drive-pulse.md` | Microcontroller AI, wearable/vehicle hardware |
| `agricultural-ugv.md` | Field robotics, sensor fusion |

### Robotics / sensors / 3D
| Project | What it proves |
|---|---|
| `aatms.md` | Built with a national space agency. Camera intrinsic/extrinsic calibration (AX=XB), 3D detection on point clouds, multi-object tracking, sub-cm calibration |
| `lidarview.md` | Velodyne/Ouster point clouds, real-time plane extraction, high-precision distance measurement |
| `arm-lift.md` | Robotic arm control |
| `newman-bands-ring-sizer.md` | Camera-only measurement validated to ±0.4mm against caliper ground truth, blind validation harness, in-browser |

### AI/ML platforms, agents, LLM
| Project | What it proves |
|---|---|
| `hoki.md` | Hierarchical multi-agent orchestration, LangGraph |
| `stackfuse.md` | AI sales platform, multi-channel outreach |
| `yes-in.md` | Scrape/enrich/qualify pipeline at scale |
| `sn3-customer-support-chatbot.md` | Production LangGraph state machine, 8-category intent classification, RAG over pgvector with RRF hybrid search, Whisper, WhatsApp Cloud API. 4-week delivery |
| `anna.md` | Annotation platform, AI suggests / human approves |
| `ideolab.md` | 6+ open sources into a single RAG layer |
| `nolmt-ai.md`, `imagate.md` | AI SaaS, AWS EKS/K8s |

### Voice AI
| Project | What it proves |
|---|---|
| `ringly.md` | Voice AI platform, $200K ARR |
| `callaxa.md`, `chatley-ai.md`, `lisa.md` | Real-time retrieval during live calls |
| `emotive-tts.md` | Custom TTS with emotional control |
| `sn3-customer-support-chatbot.md` | Whisper voice-note transcription in production |

### Generative AI / diffusion
| Project | What it proves |
|---|---|
| `ostris-masked-lora-training.md` | Sole engineer. Diagnosed masks not respected in loss computation, delivered corrected .safetensors |
| `ai-video-generation-platform.md` | LTX-2 production video inference |
| `nolmt-ai.md` | AI SaaS built on generative models |
| `3d-facial-animation.md` | Facial animation generation |

### Data platforms / annotation / synthetic data
| Project | What it proves |
|---|---|
| `anna.md` | Multi-format annotation (text, image, audio, video), AI suggests / human approves |
| `imagate.md` | Synthetic data generation platform, AWS EKS/Kubernetes |
| `well-log-digitization.md` | Document/raster digitization to structured format |

### Full-stack AI SaaS / product
| Project | What it proves |
|---|---|
| `stackfuse.md` | AI sales platform, multi-channel outreach, Series A stage |
| `nolmt-ai.md` | Full-stack AI SaaS |
| `ideolab.md` | 6+ open sources into a single RAG layer |
| `la-fragrancia.md` | Commercial product build |

### Healthcare / medical imaging
| Project | What it proves |
|---|---|
| `dyseye.md` | Browser webcam eye-tracking pipeline, live at readabletech.com |
| `jpl-dental-ai.md` | Dental imaging AI |

### VR / 3D / metaverse
| Project | What it proves |
|---|---|
| `vr-glasses.md`, `allied-bank-vr.md` | VR application development |
| `3d-facial-animation.md` | 3D character animation |
| `newman-bands-ring-sizer.md` | In-browser camera measurement, ±0.4mm vs caliper ground truth |

### Other CV / industrial
| Project | What it proves |
|---|---|
| `netauto.md`, `urban-guard.md` | Traffic monitoring, smart-city detection and tracking |
| `trackue.md` | Face recognition + eye landmark detection, edge processing |

---

## Match calibration

Score the **overlap of the actual work**, not the vocabulary.

| Band | Means | Digest behaviour |
|---|---|---|
| **>70%** | Same problem shape, same stack, comparable scale. Danish has shipped this. | Lead with the project by name and its real metric |
| **40-70%** | Genuinely transferable — same class of problem, different domain or scale | Name it as transferable, never as "I built this exact thing" |
| **<40%** | Different problem wearing similar words | **Auto-discard.** Do not surface the job at all |

**The failure mode to avoid:** a job says "tracking" and you score Trackzella at 80% without
checking whether they mean object tracking in video or tracking shipments in a database. Read
the post. Read the project file. Then score.

### ⚠️ The opposite failure: under-scoring cross-domain adjacency
**(Added 2026-09-07 after binning a job at 35% that was really 55%. Hashim caught it.)**

Over-scoring is the loud failure. **Under-scoring is the silent one**, and it costs more, because
nobody ever sees the job that was wrongly dropped.

**Read the whole post before scoring, never the snippet.** Job descriptions routinely state which
adjacent backgrounds they welcome, and that line is usually below the fold. Look for:

| Signal in the post | What it means |
|---|---|
| "or another <field>", "you might come from X, Y or Z" | Client is *actively recruiting* from adjacent fields. Score the adjacency generously |
| "X is a major plus" | If Danish has X, it outweighs a listed core skill he lacks |
| "we don't expect you to know everything" | Aptitude hire. Shape-of-problem experience beats credentials |
| "you do not need to be a <role> veteran" | Explicit invitation to cross-domain applicants |

**Score the problem shape, not the vocabulary.** Estimation, tracking, calibration, sensor fusion
and detection-under-noise all transfer across sensing modalities. The signal domain (optical,
LiDAR, RF, acoustic) is often the *smaller* difference. Isolate what genuinely does not transfer —
usually the specific hardware and toolchain — and count only that as the gap.

**The case that produced this rule:** `2096873902986486790`, Radar & Sensing Engineer (Fravek).
Scored **35% from the snippet** on "RF/SDR is a different discipline", then silently dropped. The
full post said *"or another sensing field"*, named **sensor fusion and GNSS as major pluses**, and
said *"you do not need to be a radar veteran."* Danish has two documented sensor-fusion systems
(one defence, one with a space agency), Kalman-filter target tracking, and GPS-**denied**
navigation — which is the GNSS problem. True match **55%**. The real gap was hands-on SDR/RF
hardware, listed as a requirement, and that is worth disclosing rather than hiding.

**Worked examples from real scans:**

| Job | Honest score | Why |
|---|---|---|
| Football pitch calibration + player tracking | 80% | Trackzella is literally this for another sport; homography + multi-object tracking + OpenCV all direct |
| Drone house detection, robust to seasonal drift | 75% | Satellite Imagery Analytics did aerial detection *and* chronological change comparison — the exact hard part |
| Roofline segmentation, train a U-Net | 70% | Well Log trained a U-Net from scratch on thin-structure segmentation. Different domain, identical technique |
| Long-term memory retrieval audit for an AI companion | 50% | Real-time retrieval in voice AI is adjacent, but nothing in the files is chat-memory orchestration |
| Wearable stress detection from PPG | 45% | Drive-Pulse is wearable hardware; this is biosignal feature engineering. Different discipline |
| Generative video post-training | 45% | Image-diffusion post-training yes (Ostris), video-model post-training no. Disclose the gap |
| RL model to top a benchmark leaderboard | 25% | No RLHF or SOTA-chasing work exists in the files. Discard |

---

## Reading client quality correctly

`client.rating` is **the score freelancers gave the client** — a low number means other
freelancers had a bad time. It is not a measure of the client's success. Always frame it that way.

| Pattern | Read |
|---|---|
| High spend, high hires (e.g. $27k / 179 hires) | Real repeat buyer. Best signal available |
| High spend, 1 hire | One big contract. Not proof they hire often |
| High spend, rating < 4.0 | They pay, but freelancers dislike working with them. Flag hard |
| $0 spent, verified payment | Unproven, not disqualifying. Fine for small fixed scope, risky for a big fixed bid |
| $0 spent, payment unverified | Highest risk. Only worth it on an exceptional match, and say so |
| `invitesSent` high, `totalHired` 0 | Shopping hard, may never close |
| `totalHired` > 0 while still open | Likely filling a second seat, or already decided. Heavy penalty |

### ⚠️ Two recency rules, both added 2026-09-07. Do not conflate them.

**Rule 1 — JOB age: 2 days maximum.** Hard filter in `SKILL.md`. Anything posted more than 48
hours ago is discarded before scoring, no exceptions. Hashim's standing instruction.

**Rule 2 — CLIENT activity recency: below.** Applies to jobs that pass Rule 1. A client can post a
brand-new job and still be a dormant buyer.

### ⚠️ Client activity RECENCY — check this before scoring the client at all
**(Added 2026-09-07 after a real miss. Hashim caught it.)**

**Lifetime totals say nothing about whether a client is hiring *now*.** `spend_total` and
`jobs_with_hires` are cumulative and never decay. A client with 63 hires who last started a
contract 14 months ago is not a live buyer.

**Always read `client_work_history` start dates before assigning the client score.** The sample is
the 5 most recent open and 5 most recent closed contracts *by start date*, so if the newest start
in that list is old, there genuinely are no newer ones.

| Most recent contract start | Client score treatment |
|---|---|
| Within ~3 months | Full marks available. Actively hiring |
| 3-12 months | Cap at 60% of the band. Slowing down |
| Over 12 months | **Cap at 8/25 regardless of lifetime totals.** Dormant |
| No dates returned | Score on totals but say the recency is unknown |

**Beware "active" contracts that never closed.** A high `contracts_active` count where every start
date is a year old means the client does not close contracts, not that work is ongoing. Read the
dates, not the count.

**The case that produced this rule:** job `2086178149769469238`, wall replacement, submitted
2026-09-07. Client showed $19,594 spent, 63 jobs with hires, 4.9 from 47 reviews, 13 active
contracts — scored 20/25. But all ten sampled contracts started between **May and August 2025**,
none in 2026, and the job itself had sat 30 days with 0 hires. Correct score was closer to 8/25,
which would have put the job at ~61 and below the apply threshold.

## Connects discipline

Cost scales with job value, so a bad application is expensive twice.
- Under 60 score: never worth the Connects.
- Boost only when the job is high-value *and* the current top boost bids are low. Check
  `boost.current_top_bids` in the proposal preview, never guess.
- Track balance in every digest. Below 100, say so — it changes what is worth applying to.
