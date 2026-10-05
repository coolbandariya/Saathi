# Saathi evaluation

## Intent benchmark
The repository contains a deterministic 120-case synthetic intent benchmark in backend/app/evaluation.py, with 20 cases each for farming, schemes, documents, tasks, human escalation and general conversation.

## Current benchmark status

The intent benchmark is 120 synthetic cases and the repository now also includes a 40-field farming-entity extraction benchmark. These are deterministic regression benchmarks, not claims about real-world speech accuracy.

## Required next dataset
Build a synthetic 100–200 utterance dataset covering:
- Hindi
- Hinglish
- Haryanvi-accented Hindi
- noisy speech transcripts
- ambiguous requests
- farming entities
- scheme entities
- human escalation

Measure:
- WER for speech
- intent accuracy
- farming entity exact-match / field accuracy
- entity accuracy
- tool-selection accuracy
- grounded-answer correctness
- escalation precision/recall
- end-to-end latency

Never put real phone numbers, Aadhaar, medical records, or private documents in the dataset.


## Submission-grade scorecard

Before recording the final demo, freeze provider/model versions and record:
- text intent accuracy
- farming entity exact-match and per-field accuracy
- tool-selection accuracy
- grounded-answer correctness against the returned tool payload
- escalation precision / recall
- speech WER/CER on a consented synthetic/redacted fixture set
- p50/p95 time to first transcript
- p50/p95 time to first audio
- p50/p95 end-to-end turn latency
- provider error rate and successful-turn rate

Every reported number must include dataset size, collection date, environment, provider/model version, and known limitations.
