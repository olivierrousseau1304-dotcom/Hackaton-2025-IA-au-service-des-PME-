from fastapi import APIRouter, Request, HTTPException, Depends
from pydantic import BaseModel
from starlette.responses import PlainTextResponse
from twilio.twiml.messaging_response import MessagingResponse

from ..config import settings
from ..storage.sqlite import get_conn, init_db, insert_inbound, insert_status
from ..providers.twilio_client import get_twilio_validator
from ..services.sms import send_sms

router = APIRouter(prefix="/sms", tags=["sms"])

# ---------- DTO ----------
class SendSMSRequest(BaseModel):
    to: str
    body: str

# ---------- DB ----------
def _conn():
    conn = get_conn(settings.SQLITE_PATH)
    init_db(conn)
    return conn

# ---------- Helpers ----------
def _public_url_from_request(request: Request) -> str:
    """
    Reconstruit l'URL publique pour la validation Twilio en tenant compte du reverse proxy.
    Utilise X-Forwarded-Proto et X-Forwarded-Host si présents.
    """
    headers = request.headers
    proto = headers.get("x-forwarded-proto") or request.url.scheme
    host = headers.get("x-forwarded-host") or headers.get("host") or request.url.hostname
    path = request.url.path
    query = ("?" + request.url.query) if request.url.query else ""
    return f"{proto}://{host}{path}{query}"

def _validate_twilio_signature(request: Request):
    if not settings.TWILIO_VALIDATE_SIGNATURE:
        return True
    validator = get_twilio_validator()
    signature = request.headers.get("X-Twilio-Signature")
    if not signature:
        raise HTTPException(401, "Missing Twilio signature")
    # Twilio signe l'URL exacte + les params form-encoded
    url = _public_url_from_request(request)
    form_dict = dict(request._form) if hasattr(request, "_form") else {}
    if not validator.validate(url, form_dict, signature):
        raise HTTPException(401, "Invalid Twilio signature")
    return True

# ---------- Routes ----------
@router.post("/send")
def sms_send(payload: SendSMSRequest, conn=Depends(_conn)):
    """
    Envoie un SMS. Si PUBLIC_BASE_URL est défini, configure automatiquement le status callback.
    """
    status_cb = None
    if settings.PUBLIC_BASE_URL:
        status_cb = settings.PUBLIC_BASE_URL.rstrip("/") + "/sms/status"
    result = send_sms(conn, payload.to, payload.body, status_callback_url=status_cb)
    return {"ok": True, **result}

@router.post("/inbound")
async def sms_inbound(request: Request, conn=Depends(_conn)):
    """
    Webhook pour réception de SMS. Répond par un TwiML simple et enregistre dans SQLite.
    """
    form = await request.form()
    request._form = form  # stash pour la validation
    try:
        _validate_twilio_signature(request)
    except Exception:
        if settings.TWILIO_VALIDATE_SIGNATURE:
            raise

    from_ = form.get("From")
    to = form.get("To")
    body = form.get("Body", "")

    insert_inbound(conn, from_, to, body, str(dict(form)))

    resp = MessagingResponse()
    resp.message("Bien reçu — nous revenons vers vous rapidement.")
    return PlainTextResponse(str(resp), media_type="application/xml")

@router.post("/status")
async def sms_status(request: Request, conn=Depends(_conn)):
    """
    Webhook de statut d'envoi (queued/sent/delivered/undelivered/failed).
    """
    form = await request.form()
    request._form = form
    try:
        _validate_twilio_signature(request)
    except Exception:
        if settings.TWILIO_VALIDATE_SIGNATURE:
            raise

    message_sid = form.get("MessageSid")
    message_status = form.get("MessageStatus")
    error_code = form.get("ErrorCode")
    insert_status(conn, message_sid, message_status, error_code, str(dict(form)))
    return PlainTextResponse("OK")
