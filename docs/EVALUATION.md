# Saathi evaluation

## Intent benchmark
The repository contains a deterministic 120-case synthetic intent benchmark in backend/app/evaluation.py, with 20 cases each for farming, schemes, documents, tasks, human escalation and general conversation.

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
- entity accuracy
- tool-selection accuracy
- grounded-answer correctness
- escalation precision/recall
- end-to-end latency

Never put real phone numbers, Aadhaar, medical records, or private documents in the dataset.
