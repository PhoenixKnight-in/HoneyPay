from fastapi import FastAPI
from database import create_tables
from routes.login import router as login_router

app = FastAPI(title="HoneyPay API")

# Create DB tables on startup
create_tables()

# Register routes
app.include_router(login_router)


@app.get("/")
def root():
    return {"message": "HoneyPay API is running"}