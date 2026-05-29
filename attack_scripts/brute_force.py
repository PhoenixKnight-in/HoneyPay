import requests
import time
from colorama import Fore, init

init(autoreset=True)

TARGET = "http://localhost:8001/admin/panel"
NUM_REQUESTS = 20

print(Fore.MAGENTA + "=" * 55)
print(Fore.MAGENTA + "  BRUTE FORCE ATTACK SIMULATOR")
print(Fore.MAGENTA + f"  Target: {TARGET}")
print(Fore.MAGENTA + f"  Sending {NUM_REQUESTS} requests...")
print(Fore.MAGENTA + "=" * 55)

for i in range(1, NUM_REQUESTS + 1):
    try:
        resp = requests.get(TARGET, timeout=5)
        if resp.status_code == 200:
            print(Fore.YELLOW + f"[{i:03d}] Hit: {TARGET}", end="\r")
        else:
            print(Fore.RED + f"[{i:03d}] Failed ({resp.status_code})", end="\r")
    except Exception as e:
        print(Fore.RED + f"[{i:03d}] ERROR: {e}")
    time.sleep(0.05)

print(Fore.MAGENTA + f"\n\n[DONE] Brute force complete. {NUM_REQUESTS} requests fired!")