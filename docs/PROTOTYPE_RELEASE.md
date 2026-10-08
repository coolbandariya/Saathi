# Saathi prototype release checklist

This checklist is for the **working product prototype**, not a hackathon presentation.

## User journey

- [ ] Open the product page and reach the workspace without dead links.
- [ ] Type a Hindi/Hinglish farming question and receive a grounded response.
- [ ] Try an intentionally incomplete farming question and confirm Saathi asks for the missing context instead of guessing.
- [ ] Try an explicit human-help request and confirm escalation is selected.
- [ ] Inspect source provenance, retrieval time and correlation ID on tool-backed answers.
- [ ] Confirm provider status is truthful when credentials are absent.

## Browser voice

- [ ] Serve the frontend over HTTPS in the deployed environment.
- [ ] Grant microphone permission.
- [ ] Record a short Hindi/Hinglish request.
- [ ] Verify STT transcript, specialist routing, source evidence and returned audio.
- [ ] Record first transcript, first audio and complete-turn latency.

## Real data

- [ ] Open-Meteo returns a real forecast with retrieval provenance.
- [ ] OGD/AGMARKNET returns a real daily market observation with exact commodity/location matching.
- [ ] The mandi answer exposes the source date separately from retrieval time.
- [ ] Provider failures never become invented values.

## Phone voice

- [ ] Deploy the FastAPI WebSocket endpoint behind public wss://.
- [ ] Configure Exotel AgentStream.
- [ ] Configure Sarvam Realtime STT and streaming TTS.
- [ ] Complete a real call from caller speech to spoken response.
- [ ] Verify barge-in clears active playback.
- [ ] Measure first partial transcript, final transcript, first audio and turn-complete latency.

## Release hygiene

- [ ] No secrets, Aadhaar numbers, phone numbers or private documents are committed.
- [ ] Demo/simulated state is visibly labelled.
- [ ] Supabase remains disabled until the non-Supabase vertical slice is accepted.
- [ ] Freeze the exact commit used for any public prototype demo.
