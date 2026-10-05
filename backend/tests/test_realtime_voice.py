import asyncio
import json

from app.voice_bridge import run_exotel_realtime_session


class FakeExotelWS:
    def __init__(self, events):
        self.events = events
        self.sent = []

    def __aiter__(self):
        return self

    async def __anext__(self):
        if not self.events:
            raise StopAsyncIteration
        await asyncio.sleep(0.02)
        return self.events.pop(0)

    async def send(self, value):
        self.sent.append(value)
        await asyncio.sleep(0)


class FakeRealtimeSTT:
    def __init__(self):
        self.events = [
            {"event": "vad.speech_start"},
            {"event": "transcript.final", "text": "नमस्ते"},
        ]
        self.connected_rate = None
        self.audio = []
        self.closed = False

    async def connect(self, *, sample_rate):
        self.connected_rate = sample_rate

    async def send_audio(self, pcm):
        self.audio.append(pcm)
        await asyncio.sleep(0)

    async def receive(self):
        await asyncio.sleep(0)
        if self.events:
            return self.events.pop(0)
        await asyncio.sleep(60)
        return {"event": "session.end"}

    async def close(self):
        self.closed = True


def test_realtime_bridge_forwards_pcm_and_handles_barge_in():
    async def run():
        import base64

        pcm = b"\x10\x00" * 400
        ws = FakeExotelWS([
            json.dumps({
                "event": "start",
                "start": {
                    "stream_sid": "MZ1",
                    "call_sid": "CA1",
                    "media_format": {"sample_rate": "8000"},
                },
            }),
            json.dumps({"event": "media", "media": {"payload": base64.b64encode(pcm).decode()}}),
            json.dumps({"event": "stop"}),
        ])
        stt = FakeRealtimeSTT()
        calls = []

        async def respond(text):
            calls.append(text)
            return "जी, मैं सुन रहा हूँ।"

        async def tts(text, sample_rate):
            calls.append(("tts", text, sample_rate))
            yield b"reply"

        await run_exotel_realtime_session(
            ws,
            stt_session=stt,
            respond=respond,
            synthesize_stream=tts,
        )

        assert stt.connected_rate == 8000
        assert stt.audio == [pcm]
        assert calls[0] == "नमस्ते"
        assert any(json.loads(item).get("event") == "clear" for item in ws.sent)
        assert stt.closed

    asyncio.run(run())
