from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import traps, bridge
import models  # noqa: F401

app = FastAPI(
    title="HoneyPay Honeypot Service",
    description="Trap service — all endpoints are deceptive",
    version="1.0.0"
)

# CORS — allows React dashboard to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(traps.router)
app.include_router(bridge.router)


@app.get("/health")
def health_check():
    return {"status": "honeypot running", "port": 8001}