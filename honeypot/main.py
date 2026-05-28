from fastapi import FastAPI
from database import engine, Base
from routers import traps
import models  # noqa: F401

app = FastAPI(
    title="HoneyPay Honeypot Service",
    description="Trap service — all endpoints are deceptive",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(traps.router)


@app.get("/health")
def health_check():
    return {"status": "honeypot running", "port": 8001}