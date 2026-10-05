# Saathi demo runbook

## Golden path
1. Open the operator dashboard.
2. Start the demo call.
3. Speak in Hindi: “गेहूं का मंडी भाव क्या है?”
4. Show the farming agent selection.
5. Show the tool result and provenance.
6. Ask: “कल बारिश होगी?”
7. Show the weather tool result.
8. Ask a scheme question.
9. Escalate an intentionally ambiguous request to human support.

## Truthfulness rules
- Never call simulated data live data.
- Never claim a real phone call unless the telephony provider is configured and the call was actually placed.
- Never claim an application was submitted unless the official integration confirms it.
- Never expose secrets in screenshots or recordings.
