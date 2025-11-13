from fastapi import FastAPI
from .routers import sms, health

app = FastAPI(title="Hackprint – Twilio SMS")

# Routes
app.include_router(health.router)
app.include_router(sms.router)
