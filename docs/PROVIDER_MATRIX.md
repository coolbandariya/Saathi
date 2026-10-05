# Provider Matrix

Providers are replaceable adapters. The MVP should not hard-wire business logic to one vendor.

| Capability | Primary direction | Fallback/demo |
|---|---|---|
| LLM | Gemini/OpenAI adapter | deterministic demo responder |
| STT | Bhashini / compatible speech adapter | browser/demo transcript |
| TTS | Bhashini / compatible speech adapter | browser speech or text |
| Telephony | Exotel or validated Indian provider | browser call simulation |
| Database | Supabase/Postgres | local deterministic fixtures |
| Weather | Open-Meteo or validated source | timestamped demo fixture |
| Mandi | official/validated agriculture source | timestamped demo fixture |
| OCR | Bhashini/compatible OCR | fixture OCR in demo |

Every factual provider response must carry source/timestamp metadata internally so stale or missing data can be handled explicitly.
