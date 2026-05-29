import redis
import os
from dotenv import load_dotenv
from fastapi import Request, HTTPException, status

load_dotenv()

try:
    r = redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        db=0,
        decode_responses=True
    )
    r.ping()
    REDIS_AVAILABLE = True
    print("✅ Redis connected — Rate limiting enabled")
except Exception as e:
    REDIS_AVAILABLE = False
    print(f"⚠️  Redis unavailable — Rate limiting disabled: {e}")

# Thresholds
MAX_FAILED_ATTEMPTS = 5
BLOCK_WINDOW = 60  # seconds


def check_rate_limit(request: Request, success: bool):
    """
    Call this after every login attempt.
    - On failure: increment the counter
    - On success: reset the counter
    - When counter exceeds limit: raise 429
    """
    if not REDIS_AVAILABLE:
        return

    ip = request.client.host
    key = f"rl:{ip}"

    if success:
        # Successful login — clear their failed attempt counter
        r.delete(key)
        return

    # Failed login — increment counter
    count = r.incr(key)
    if count == 1:
        r.expire(key, BLOCK_WINDOW)

    print(f"[RATE LIMIT] {ip} → failed attempts: {count}/{MAX_FAILED_ATTEMPTS}")

    if count > MAX_FAILED_ATTEMPTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many failed attempts. Try again later.",
            headers={"Retry-After": str(BLOCK_WINDOW)}
        )