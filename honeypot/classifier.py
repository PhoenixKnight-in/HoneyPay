import redis
import os
from dotenv import load_dotenv

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
    print("✅ Redis connected — Brute Force detection enabled")
except Exception as e:
    REDIS_AVAILABLE = False
    print(f"⚠️  Redis unavailable — Brute Force detection disabled: {e}")


SQL_INJECTION_PATTERNS = [
    "' or '1'='1",
    "or 1=1",
    "union select",
    "drop table",
    "insert into",
    "sleep(",
    "benchmark(",
    "xp_cmdshell",
    ";--",
    "' --",
    "1=1--",
    # Add these missing patterns
    "--",
    "' #",
    "admin' #",
    "or 'x'='x",
    "' or 'x'",
    "1' or '1'",
    "or '1' =",
    "'/*",
    "1=1/*",
]

RECON_PATHS = [
    "/admin", "/config", "/.env", "/.git",
    "/env", "/backup", "/phpmyadmin",
    "/internal", "/root", "/db", "/dump", "/users/all",
]

SCANNER_USER_AGENTS = [
    "nikto", "sqlmap", "burpsuite", "nmap",
    "masscan", "zgrab", "python-requests",
    "curl", "scanner", "dirbuster", "gobuster",
]

BRUTE_FORCE_LIMIT = 10
BRUTE_FORCE_WINDOW = 120     # increased to 2 minutes
SCANNER_ENDPOINT_LIMIT = 5
SCANNER_TIME_WINDOW = 30


def classify_attack(
    ip_address: str,
    endpoint: str,
    payload: str,
    user_agent: str
) -> str:

    # 1. SQL Injection
    if payload:
        payload_lower = payload.lower()
        for pattern in SQL_INJECTION_PATTERNS:
            if pattern in payload_lower:
                return "SQL Injection"

    # 2. Brute Force
    if REDIS_AVAILABLE:
        key = f"bf:{ip_address}"
        try:
            count = r.incr(key)
            if count == 1:
                r.expire(key, BRUTE_FORCE_WINDOW)
            if count > BRUTE_FORCE_LIMIT:
                return "Brute Force"
        except Exception as e:
            print(f"[REDIS ERROR] {e}")

    # 3. Scanner — user agent
    if user_agent:
        ua_lower = user_agent.lower()
        for agent in SCANNER_USER_AGENTS:
            if agent in ua_lower:
                return "Scanner"

    # 4. Scanner — endpoint diversity
    if REDIS_AVAILABLE:
        try:
            diversity_key = f"scan:{ip_address}"
            r.sadd(diversity_key, endpoint)
            r.expire(diversity_key, SCANNER_TIME_WINDOW)
            unique_endpoints = r.scard(diversity_key)
            if unique_endpoints >= SCANNER_ENDPOINT_LIMIT:
                return "Scanner"
        except Exception as e:
            print(f"[REDIS ERROR] {e}")

    # 5. Recon — default
    return "Recon"