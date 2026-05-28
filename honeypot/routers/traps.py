from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import AttackLog
from classifier import classify_attack
import json

router = APIRouter(tags=["Honeypot Traps"])


async def log_attack(request: Request, db: Session, endpoint: str):
    """
    Central logging function called by every trap endpoint.
    Extracts request metadata, classifies the attack, writes to DB.
    """
    ip_address = request.client.host
    user_agent = request.headers.get("user-agent", "")

    # Extract payload from body if present
    payload = None
    try:
        body = await request.body()
        if body:
            payload = body.decode("utf-8")
    except Exception:
        payload = None

    attack_type = classify_attack(
        ip_address=ip_address,
        endpoint=endpoint,
        payload=payload or "",
        user_agent=user_agent
    )

    log_entry = AttackLog(
        ip_address=ip_address,
        endpoint=endpoint,
        payload=payload,
        attack_type=attack_type,
        user_agent=user_agent
    )
    db.add(log_entry)
    db.commit()

    return attack_type


# ── Trap 1: Admin Panel ─────────────────────────────────────────────
@router.get("/admin/panel")
async def fake_admin_panel(request: Request, db: Session = Depends(get_db)):
    attack_type = await log_attack(request, db, "/admin/panel")
    return {
        "status": "authorized",
        "role": "superadmin",
        "users_count": 10482,
        "total_balance": "Rs. 84,20,000",
        "server": "prod-db-01",
        "_detected": attack_type       # invisible to real attacker in prod
    }


# ── Trap 2: DB Dump ─────────────────────────────────────────────────
@router.get("/api/internal/db/dump")
async def fake_db_dump(request: Request, db: Session = Depends(get_db)):
    attack_type = await log_attack(request, db, "/api/internal/db/dump")
    return {
        "status": "success",
        "tables": ["users", "transactions", "audit_logs"],
        "row_count": 84291,
        "dump_url": "s3://honeypay-prod/dumps/latest.sql.gz"
    }


# ── Trap 3: Root Override ───────────────────────────────────────────
@router.post("/api/root/override")
async def fake_root_override(request: Request, db: Session = Depends(get_db)):
    attack_type = await log_attack(request, db, "/api/root/override")
    return {
        "status": "override accepted",
        "privilege": "root",
        "message": "System access granted"
    }


# ── Trap 4: Env Config ──────────────────────────────────────────────
@router.get("/config/env")
async def fake_env_config(request: Request, db: Session = Depends(get_db)):
    attack_type = await log_attack(request, db, "/config/env")
    return {
        "DB_HOST": "prod-db-01.internal",
        "DB_PASS": "s3cr3t_prod_p@ss",
        "JWT_SECRET": "prod-jwt-key-do-not-share",
        "ENV": "production"
    }


# ── Trap 5: User Dump ───────────────────────────────────────────────
@router.get("/api/v1/users/all")
async def fake_user_dump(request: Request, db: Session = Depends(get_db)):
    attack_type = await log_attack(request, db, "/api/v1/users/all")
    return {
        "status": "success",
        "count": 10482,
        "users": [
            {"id": 1, "username": "admin", "email": "admin@honeypay.in", "balance": 9999999},
            {"id": 2, "username": "superuser", "email": "su@honeypay.in", "balance": 500000},
        ]
    }