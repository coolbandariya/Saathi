# Provider Matrix

| Capability | Implemented now | Production target | Safety rule |
|---|---|---|---|
| LLM | Demo + Gemini adapter | Gemini/OpenAI | Tool calls only for factual/action work |
| STT | Protocol + deterministic demo | Bhashini/Whisper adapter | Confidence + language metadata |
| TTS | Protocol + deterministic demo | Bhashini TTS | Never log audio contents |
| Telephony | Exotel protocol/client | Exotel AgentStream | WSS, signature/replay protection |
| Weather | Open-Meteo adapter | Open-Meteo/IMD adapter | Coordinates + timestamp required |
| Mandi | Data.gov.in configurable adapter | Official agriculture data resource | Commodity/market validation + source timestamp |
| Schemes | myScheme-backed PM-USP evaluator | Versioned catalogue ingestion | Deterministic eligibility |
| OCR | Upload/review boundary | Bhashini/compatible OCR | Confidence threshold + human review |
| Database | In-memory test repository | Supabase/Postgres | RLS + consent + audit |

External providers remain replaceable and credentials stay server-side.
