from fastapi import FastAPI
from database import engine, Base
from routers import auth, accounts
# Import models so Base knows about them before create_all
import models  # noqa: F401

app = FastAPI(
    title="HoneyPay Payment API",
    description="Secure fintech API with honeypot detection",
    version="1.0.0"
)

# Create all tables on startup
Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(auth.router)
app.include_router(accounts.router)

@app.get("/health")
def health_check():
    return {"status": "payment_api running", "port": 8000}