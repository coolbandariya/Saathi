# Saathi — Hackathon Win Plan

Updated: 2026-10-06

## Strategic position

**Research checkpoint: 2026-10-06.** JAI is the hard deadline: Unstop currently lists registration by 10 Oct 2026 11:59 PM IST and Round 1 project/prototype submission by 15 Oct; the official summit confirms the offline event is 30–31 Oct. Tech Eximius 2.0 currently lists 2–4 members, a mandatory GoPass verification task, a maximum-six-slide PPT, and an 8-hour offline final. Its public listings currently show conflicting registration deadlines, so the team should treat the deadline displayed in its active Unstop submission flow as authoritative and submit well before it.

Saathi should enter both competitions with the same core product, but tell two different stories.

### JAI 2026 — primary track: Agentic AI for NLP

**Positioning:** a Hindi/Hinglish voice agent that understands messy natural-language requests, extracts entities, selects verified specialist tools, grounds answers in authoritative data, and escalates when it cannot answer safely.

The product should demonstrate:
- multilingual / code-mixed speech
- intent classification
- entity extraction
- deterministic fallback
- allow-listed tool calling
- authoritative source grounding
- human escalation
- observable evidence

Open Innovation is the secondary fit because the same agent addresses a real-world accessibility problem with APIs and autonomous tool use.

### Tech Eximius 2.0 — primary story: AI + Social Impact / Open Innovation

**Positioning:** voice-first access to useful public information for people who are more comfortable speaking Hindi than navigating complex digital portals.

Emphasize:
- accessibility
- real government/market/weather data
- low-friction voice interaction
- source provenance
- safety boundaries
- scalability across Indian languages and domains

## The one memorable demo

A farmer calls/opens Saathi and says, in natural Hinglish:

"Kal Sonipat mein गेहूं ka mandi bhav kya hai? Baarish ka chance bhi batao."

Saathi should:
1. transcribe speech;
2. classify farming intent;
3. extract commodity = Wheat, district = Sonipat, state = Haryana;
4. resolve location explicitly for weather;
5. call AGMARKNET and Open-Meteo;
6. display both sources and retrieval times;
7. answer in Hindi;
8. synthesize the response;
9. show a correlation ID / event timeline;
10. refuse to invent data if either source fails.

Second short interaction:
"Insaan se baat karni hai."

Saathi immediately demonstrates human escalation.

This single story covers NLP, tool use, grounding, multilingual UX, safety and real-world impact.

## Architecture judges should see

Caller/browser
-> speech input
-> Sarvam STT
-> deterministic intent/entity layer
-> specialist tool router
-> authoritative API
-> provenance contract
-> response policy
-> Sarvam TTS
-> caller/browser

Gemini is optional for ambiguous routing only. It must never be the factual authority.

Specialist tools:
- weather: Open-Meteo
- mandi: Government OGD / AGMARKNET
- future schemes: versioned government source catalogue
- human: escalation workflow

## Non-negotiable evidence

Every live answer should expose:
- source name
- source URL
- retrieval timestamp
- freshness note
- correlation ID
- tool selected
- latency

The demo must visibly distinguish LIVE from SIMULATED.

## Metrics to collect before submission

### NLP
- intent accuracy
- entity exact-match / partial-match accuracy
- tool-selection accuracy
- grounded-answer correctness
- escalation precision / recall

### Voice
- word error rate / character error rate
- time to first transcript
- time to first audio
- complete turn latency
- failed-turn rate

### Reliability
- provider error rate
- successful end-to-end turn rate
- p50/p95 latency
- malformed-input rejection rate

A benchmark report should contain the test-set size, date, model/provider versions, methodology and known limitations.

## JAI under-5-minute video

Target 4:20–4:40, not 4:59.

0:00–0:20 — team + problem
0:20–1:20 — live voice interaction
1:20–2:20 — show transcript, intent, entities, tools and provenance
2:20–3:10 — show human escalation and failure-safe behavior
3:10–3:50 — architecture + why this is agentic
3:50–4:25 — metrics + repository ownership
4:25–4:40 — team contributions + closing

Do not spend the first minute on slides.

## Tech Eximius six-slide deck

### 1. Saathi
Team, project name, GitHub, live prototype, demo video.

### 2. Problem
Language, literacy and portal-friction barriers; explain why existing chatbot-style interfaces are insufficient.

### 3. Solution
Voice-first multilingual agent with deterministic routing, specialist tools, provenance and human fallback.

### 4. Workflow + technical implementation
One diagram from speech to verified tool to spoken response. Include real technologies and boundaries.

### 5. USP + evidence
- Hindi/Hinglish understanding
- source-grounded answers
- live APIs
- safety / escalation
- measured latency and accuracy
- no fabricated facts

### 6. Impact + scale
India-wide language expansion, reusable provider adapters, government-data connectors, phone accessibility, privacy/consent architecture.

## What will make judges skeptical

Never claim:
- realtime phone AI before a genuine Exotel call;
- live data when demo data is simulated;
- Haryanvi understanding without a benchmark;
- autonomous government submission;
- medical diagnosis;
- "multi-agent" merely because multiple functions exist;
- high accuracy without a measured evaluation set.

## Judge-winning upgrades discovered in current research

1. **Make the agent visibly agentic, not merely routed.** Show a planner/tool decision, tool execution, evidence returned, and response policy. Gemini Interactions is now GA and explicitly supports structured tool calls; keep execution in Saathi so the model remains a planner rather than the source of truth.
2. **Make voice genuinely real before claiming phone intelligence.** Sarvam Realtime STT supports partial/final transcripts, server VAD, `speech_start`/`speech_end`, and `flush`; Saaras v4 supports keyterm prompting. Exotel AgentStream supports bidirectional PCM and `clear` for barge-in.
3. **Make the farming story unusually trustworthy.** The government mandi dataset is daily-granularity AGMARKNET data, so Saathi should say “latest government-reported market observation” and expose the observation date—not imply tick-level or guaranteed same-day availability.
4. **Turn evaluation into a competitive asset.** Report intent, entity, tool-selection, grounded-answer, escalation, WER, first-transcript, first-audio and p50/p95 turn latency with provider/model versions and test-set date.
5. **Design for judge interruption.** Every demo step needs a fallback: preloaded demo route if provider fails, visible LIVE/DEMO state, and a 20-second deterministic “proof mode” that never fabricates a live answer.

## Build priority

### Gate A — now
- CI green
- real browser Sarvam STT/TTS
- real Open-Meteo
- real AGMARKNET
- exact entity routing
- visible provenance
- benchmark report

### Gate B
- public deployment
- real Exotel call
- latency instrumentation
- call/session correlation
- synthetic audio regression set

### Gate C
- Sarvam realtime STT
- provider VAD
- streaming TTS
- barge-in with Exotel clear
- reconnect/failover

### Gate D — only after Gates A-C
- Supabase repositories
- RLS / tenant isolation
- durable memory
- reminders
- volunteer cases

## Team ownership evidence

The repository should preserve:
- meaningful commit history
- issue/PR discussion
- architecture decisions
- benchmark commits
- test additions
- deployment configuration
- named contribution areas

The JAI video should show the actual team and briefly identify each member's implementation contribution.

## Definition of "win-ready"

Saathi is win-ready when a judge can independently verify, in one sitting:

1. a real user speaks naturally;
2. Saathi understands the request;
3. the correct entities are extracted;
4. the correct authoritative tool is called;
5. the answer is grounded in returned data;
6. the source is visible;
7. the answer is spoken back;
8. an unsafe/ambiguous request escalates;
9. metrics demonstrate engineering quality;
10. the Git repository proves the team built it.

The product story is not "we built many AI features."

It is:

**"We built a voice agent that turns natural Hindi speech into verified action without letting the model invent the facts."**
