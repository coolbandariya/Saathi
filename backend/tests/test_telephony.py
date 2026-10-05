from app.telephony import HmacWebhookVerifier
import base64, hashlib, hmac

def test_hmac_webhook_verifier():
    body=b'{"event":"call"}'
    secret="secret"
    digest=base64.b64encode(hmac.new(secret.encode(),body,hashlib.sha256).digest()).decode()
    assert HmacWebhookVerifier(secret).verify(body,digest)
    assert not HmacWebhookVerifier(secret).verify(body,"bad")
