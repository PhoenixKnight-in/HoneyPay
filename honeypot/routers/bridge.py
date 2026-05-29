from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import AttackLog
from datetime import datetime, timedelta

router = APIRouter(prefix="/api", tags=["Dashboard Bridge"])


@router.get("/logs")
def get_logs(
    db: Session = Depends(get_db),
    attack_type: str = Query(None),
    limit: int = Query(50),
    since: str = Query(None)   # e.g. "1h", "24h"
):
    """Return recent attack logs with optional filters."""
    query = db.query(AttackLog)

    if attack_type:
        query = query.filter(AttackLog.attack_type == attack_type)

    if since:
        hours = int(since.replace("h", ""))
        since_time = datetime.utcnow() - timedelta(hours=hours)
        query = query.filter(AttackLog.timestamp >= since_time)

    logs = query.order_by(AttackLog.timestamp.desc()).limit(limit).all()

    return [
        {
            "id": log.id,
            "ip_address": log.ip_address,
            "endpoint": log.endpoint,
            "payload": log.payload,
            "attack_type": log.attack_type,
            "user_agent": log.user_agent,
            "timestamp": log.timestamp.isoformat() if log.timestamp else None
        }
        for log in logs
    ]


@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """Return aggregated attack statistics for the dashboard."""

    # Total attack count
    total = db.query(func.count(AttackLog.id)).scalar()

    # Count by attack type
    by_type = db.query(
        AttackLog.attack_type,
        func.count(AttackLog.id).label("count")
    ).group_by(AttackLog.attack_type).all()

    # Top 5 attacker IPs
    top_ips = db.query(
        AttackLog.ip_address,
        func.count(AttackLog.id).label("count")
    ).group_by(AttackLog.ip_address)\
     .order_by(func.count(AttackLog.id).desc())\
     .limit(5).all()

    # Hourly volume for last 24 hours
    since_24h = datetime.utcnow() - timedelta(hours=24)
    hourly_logs = db.query(AttackLog).filter(
        AttackLog.timestamp >= since_24h
    ).all()

    # Group by hour manually
    hourly_counts = {}
    for log in hourly_logs:
        if log.timestamp:
            hour_key = log.timestamp.strftime("%Y-%m-%dT%H:00:00")
            hourly_counts[hour_key] = hourly_counts.get(hour_key, 0) + 1

    hourly = [
        {"hour": hour, "count": count}
        for hour, count in sorted(hourly_counts.items())
    ]

    return {
        "total": total,
        "by_type": [
            {"attack_type": row.attack_type, "count": row.count}
            for row in by_type
        ],
        "top_ips": [
            {"ip_address": row.ip_address, "count": row.count}
            for row in top_ips
        ],
        "hourly": hourly
    }