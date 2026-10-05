# Demo Contract

The browser demo now exercises the FastAPI conversation boundary rather than showing a fake alert.

The final hackathon golden path should prove:

1. A user starts with a Hindi request.
2. The request is routed to a specialist intent.
3. A factual tool returns source/timestamp metadata.
4. A consent-gated task is created in the persistence layer.
5. The same household resumes the task.
6. A due task becomes callback-eligible only when outbound consent and quiet-hour checks pass.
7. An uncertain/unsupported case becomes a volunteer support case with transcript/context.

Anything not backed by a live provider must be labeled DEMO or SIMULATED.
