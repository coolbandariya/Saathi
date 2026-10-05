import base64
import json
from app.exotel_stream import decode_media, encode_clear, encode_mark, encode_media, parse_start

def test_parse_exotel_start_and_pcm():
    event = {"event":"start","stream_sid":"MZ1","start":{"stream_sid":"MZ1","call_sid":"CA1","from":"+9199","to":"+9188","media_format":{"encoding":"audio/x-raw","sample_rate":"8000","bit_rate":"16"}}}
    start = parse_start(event)
    assert start.sample_rate == 8000
    assert start.call_sid == "CA1"
    assert decode_media({"media":{"payload":base64.b64encode(b"abc").decode()}}) == b"abc"

def test_exotel_outbound_events():
    assert json.loads(encode_media("MZ1", b"abc"))["event"] == "media"
    assert json.loads(encode_mark("MZ1", "turn-1"))["mark"]["name"] == "turn-1"
    assert json.loads(encode_clear("MZ1"))["event"] == "clear"
