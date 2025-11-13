from typing import Optional
from ..config import settings
from ..providers.twilio_client import get_twilio_client
from ..storage.sqlite import insert_outbound

def send_sms(conn, to: str, body: str, status_callback_url: Optional[str] = None) -> dict:
    """
    Envoie un SMS via Twilio (Messaging Service si défini, sinon numéro FROM).
    Loggue l'envoi dans SQLite.
    """
    client = get_twilio_client()
    params = {"to": to, "body": body}
    if status_callback_url:
        params["status_callback"] = status_callback_url

    if settings.TWILIO_MESSAGING_SERVICE_SID:
        params["messaging_service_sid"] = settings.TWILIO_MESSAGING_SERVICE_SID
    else:
        if not settings.TWILIO_FROM_NUMBER:
            raise RuntimeError("Configure TWILIO_FROM_NUMBER or TWILIO_MESSAGING_SERVICE_SID")
        params["from_"] = settings.TWILIO_FROM_NUMBER

    msg = client.messages.create(**params)
    insert_outbound(conn, to, body, msg.sid, "queued")
    return {"sid": msg.sid}
