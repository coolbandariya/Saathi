# Saathi Failure Matrix

Saathi is designed to fail closed: when a required fact cannot be verified, it asks for missing context, retries a provider when safe, or escalates rather than inventing an answer.

| Failure | Detection | User-facing behavior | Production action |
|---|---|---|---|
| Unclear speech | STT error / incomplete transcript | Ask the caller to repeat | Retry STT once, then offer text/human fallback |
| Missing farming entity | Required commodity/state/district absent | Ask only for the missing field(s) | Preserve turn state |
| Mandi source unavailable | Provider timeout/error | Say the price could not be verified | Retry with bounded timeout; never substitute a guess |
| Mandi entity mismatch | Returned record fails entity score | Do not present the row as the requested market | Ask for market/district clarification |
| Weather location missing | No caller-provided location | Ask for district/city | Resolve location only from explicit user-provided context |
| Weather provider failure | HTTP/provider error | Say weather is unavailable | Retry safely; no fabricated forecast |
| Conflicting sources | Multiple incompatible verified observations | Surface the conflict | Require deterministic selection rule or clarification |
| TTS failure | Streaming/bounded TTS error | Return text when the channel permits | Retry once; preserve transcript and outcome |
| Caller barge-in | VAD speech start during playback | Stop current audio and listen | Send telephony `clear`; measure stop latency |
| Human request | Explicit human intent | Start handoff path immediately | Persist case only after consent/persistence integration |
| Low confidence | Policy confidence threshold | Clarify or escalate | Tune threshold against evaluation set |
| Sensitive action requested | Safety/policy boundary | Explain limitation and redirect | Never claim an external action happened |
| Demo provider active | `DEMO_MODE` | Clearly label synthetic data | Never call demo data “live” |
| No live source attached | Missing provenance | Refuse to present answer as verified fact | Treat missing provenance as release-blocking for factual tools |

## Release rule

A factual capability is **LIVE** only after its real provider path has been exercised end-to-end in the deployed environment and its observed latency/error behavior has been recorded. Configuration alone does not qualify as live.

## Voice release gate

Before recording the competition demo, verify:

1. Real phone connection.
2. Hindi/Hinglish realtime transcript.
3. Tool call from a spoken request.
4. Streaming TTS back to the caller.
5. Barge-in cuts playback.
6. A second request after barge-in is handled correctly.
7. Combined mandi + weather returns two provenance records.
8. Provider failure produces a truthful fallback.
9. Human request reaches the configured handoff path, or is explicitly labelled as simulation.
10. p50/p95 latency measurements are captured from the same deployment used for the demo.