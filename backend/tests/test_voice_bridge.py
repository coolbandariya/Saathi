import asyncio
import json
from app.voice_bridge import run_exotel_session

class FakeWS:
    def __init__(self, events):
        self.events=events
        self.sent=[]
    def __aiter__(self):
        return self
    async def __anext__(self):
        if not self.events:
            raise StopAsyncIteration
        return self.events.pop(0)
    async def send(self, value):
        self.sent.append(value)

def test_voice_bridge_uses_injected_pipeline():
    async def run():
        import base64
        pcm=base64.b64encode(b"a"*16000).decode()
        ws=FakeWS([
            json.dumps({"event":"start","start":{"stream_sid":"MZ1","call_sid":"CA1","media_format":{"sample_rate":"8000"}}}),
            json.dumps({"event":"media","media":{"payload":pcm}}),
            json.dumps({"event":"stop"}),
        ])
        calls=[]
        async def stt(audio, rate): calls.append(("stt",len(audio),rate)); return "मंडी का भाव"
        async def respond(text): calls.append(("llm",text)); return "सत्यापित डेटा उपलब्ध नहीं है।"
        async def tts(text, rate): calls.append(("tts",text,rate)); return b"reply"
        await run_exotel_session(ws,transcribe=stt,respond=respond,synthesize=tts)
        assert calls[0][0]=="stt"
        assert calls[1][0]=="llm"
        assert calls[2][0]=="tts"
        assert ws.sent

    asyncio.run(run())
