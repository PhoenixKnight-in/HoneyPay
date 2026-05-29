import requests
import time
from colorama import Fore, init

init(autoreset=True)

BASE = "http://localhost:8001"

PATHS = [
    "/admin/panel", "/admin", "/admin/login",
    "/api/internal/db/dump", "/api/root/override",
    "/config/env", "/api/v1/users/all",
    "/.git/config", "/.env", "/config.yaml",
    "/api/debug", "/api/health", "/metrics",
    "/api/v2/users", "/api/v1/admin",
    "/phpinfo.php", "/wp-admin", "/manager",
    "/api/token", "/oauth/token",
    "/actuator/env", "/actuator/health",
]

print(Fore.BLUE + "=" * 55)
print(Fore.BLUE + "  RECON / ENUMERATION SCANNER SIMULATOR")
print(Fore.BLUE + f"  Target: {BASE}")
print(Fore.BLUE + "=" * 55)

for path in PATHS:
    url = BASE + path
    try:
        resp = requests.get(url, timeout=5,
                            headers={"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1)"})
        color = Fore.GREEN if resp.status_code == 200 else Fore.YELLOW
        print(f"{color}[{resp.status_code}] {path.ljust(35)} → Responded")
    except Exception as e:
        print(Fore.RED + f"[ERR] {path.ljust(35)} → {e}")
    time.sleep(0.2)

print(Fore.BLUE + "\n[DONE] Recon scan complete!")