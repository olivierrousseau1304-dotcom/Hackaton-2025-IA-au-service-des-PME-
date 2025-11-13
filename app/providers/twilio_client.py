from twilio.rest import Client
from twilio.request_validator import RequestValidator
from ..config import settings

def get_twilio_client() -> Client:
    """
    Initialise le client Twilio avec les credentials d'environnement.
    """
    if not (settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN):
        raise RuntimeError("Twilio credentials missing (TWILIO_ACCOUNT_SID/TWILIO_AUTH_TOKEN)")
    return Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

def get_twilio_validator() -> RequestValidator:
    """
    Crée un validateur de signature Twilio.
    """
    if not settings.TWILIO_AUTH_TOKEN:
        raise RuntimeError("Twilio AUTH token missing for signature validation")
    return RequestValidator(settings.TWILIO_AUTH_TOKEN)
