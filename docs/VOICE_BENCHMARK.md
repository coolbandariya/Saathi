# Saathi Voice Benchmark

This benchmark is for the real Exotel + Sarvam vertical slice. Synthetic adapter tests validate contracts; they are not substitutes for provider measurements.

## Required test matrix

Run at least 30 turns per scenario after deployment:

| Scenario | Utterances | What to measure |
|---|---:|---|
| Hindi farming | 10 | STT, entity accuracy, tool selection |
| Hinglish farming | 10 | code-mix STT, entity accuracy |
| Combined mandi + weather | 5 | multi-tool completion, provenance |
| Missing entities | 3 | clarification precision |
| Human escalation | 2 | escalation latency |
| Barge-in | 5 | stop latency + recovery |

## Timing points

Capture timestamps for:

- Exotel media/session start
- first STT partial
- final STT transcript
- intent/tool decision
- first provider result
- first TTS audio chunk
- final TTS audio
- turn completion
- barge-in detected
- playback cleared

Report p50 and p95, not only averages.

## Quality metrics

- STT WER/CER on manually transcribed samples
- farming entity exact match and per-field accuracy
- tool-selection accuracy
- grounded-answer correctness
- clarification precision
- escalation precision/recall
- successful-turn rate
- provider error rate
- first-audio latency
- end-to-end latency
- barge-in stop latency
- post-barge-in recovery success

## Evidence format

Every published number must include:

- sample count
- collection date
- deployment/environment
- provider/model versions
- audio sample rate
- language mix
- known limitations

Never publish simulated or adapter-test timings as production voice metrics.

## Release gate

A real voice demo is ready only when:

1. 30+ real turns have been captured.
2. No fabricated source-backed answers are observed.
3. Combined mandi + weather returns both evidence paths when both providers succeed.
4. Provider failure is disclosed without inventing a value.
5. Barge-in stops playback and the next utterance is processed.
6. p50/p95 first-audio and end-to-end latency are recorded.
7. At least one raw call trace can be replayed for judging/debugging.
