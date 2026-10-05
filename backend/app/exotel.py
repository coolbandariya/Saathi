import httpx

class ExotelVoiceClient:
    def __init__(self, api_key: str, api_token: str, account_sid: str, base_url: str = "https://api.in.exotel.com", timeout: float = 8.0) -> None:
        self.api_key=api_key; self.api_token=api_token; self.account_sid=account_sid; self.base_url=base_url.rstrip("/"); self.timeout=timeout

    def connect_voice_ai(self, caller_id: str, to: str, stream_url: str, record: bool = False) -> dict:
        if not stream_url.startswith("wss://"):
            raise ValueError("stream_url must use wss://")
        url=f"{self.base_url}/v1/Accounts/{self.account_sid}/Calls/connect"
        data={"From":to,"CallerId":caller_id,"StreamUrl":stream_url,"StreamType":"bidirectional","Record":str(record).lower()}
        response=httpx.post(url,auth=(self.api_key,self.api_token),data=data,timeout=self.timeout)
        response.raise_for_status()
        return response.json()
