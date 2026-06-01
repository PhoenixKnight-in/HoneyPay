# HoneyPay — Secure Fintech API with Attack Simulator & Honeypot

> A payment API that simulates real-world cyberattacks, detects them using a smart honeypot system, and visualizes attack data on a live dashboard.

---

## What This Project Does

HoneyPay is a controlled cybersecurity environment built around a realistic fintech backend. It simulates, detects, and classifies real-world attack patterns in real time.

Three services work together:

| Component | Description | Port |
|---|---|---|
| **Payment API** | Secured FastAPI backend with login, transfer, and balance endpoints | 8000 |
| **Honeypot Service** | Fake trap endpoints that log and auto-classify attacker behavior | 8001 |
| **React Dashboard** | Live visualization of attack data, charts, and attacker IPs | 3000 |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.10 + FastAPI |
| Database | PostgreSQL + SQLAlchemy ORM |
| Rate Limiting | Redis (Memurai on Windows) |
| Frontend | React 19 + Recharts |
| Attack Scripts | Python + requests + colorama |

---

## Project Structure

```
HoneyPay/
├── payment_api/          # Secured payment backend (Port 8000)
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── dependencies.py
│   ├── routers/
│   │   ├── auth.py       # POST /api/login
│   │   └── accounts.py   # GET /api/balance, POST /api/transfer, GET /api/transactions
│   └── core/
│       ├── security.py   # bcrypt + JWT
│       └── rate_limiter.py  # Redis rate limiting
│
├── honeypot/             # Trap service (Port 8001)
│   ├── main.py
│   ├── classifier.py     # Attack classification engine
│   ├── models.py
│   └── routers/
│       ├── traps.py      # 5 fake trap endpoints
│       └── bridge.py     # /api/stats, /api/logs for dashboard
│
├── attack_scripts/       # Attack simulators
│   ├── sql_injection.py
│   ├── brute_force.py
│   └── recon.py
│
└── dashboard/            # React frontend
    └── src/
        └── components/
```

---

## Payment API Endpoints

```
POST  /api/login          →  Authenticate and receive JWT token
GET   /api/balance        →  View account balance (auth required)
POST  /api/transfer       →  Transfer funds to another user (auth required)
GET   /api/transactions   →  View transaction history (auth required)
```

**Security measures on every endpoint:**
- Parameterized queries via SQLAlchemy — no raw SQL
- bcrypt password hashing
- JWT authentication
- Input validation via Pydantic schemas
- Redis rate limiting — 429 after 5 failed login attempts in 60 seconds
- Generic error messages — never reveals which field failed

---

## Honeypot Endpoints

All five endpoints return convincing fake responses while silently logging the attacker:

```
GET   /admin/panel            →  Fake admin dashboard
GET   /api/internal/db/dump   →  Fake database dump
POST  /api/root/override      →  Fake privilege escalation
GET   /config/env             →  Fake environment config
GET   /api/v1/users/all       →  Fake user data dump
```

Every hit logs: IP address, endpoint, payload, user-agent, timestamp, and attack classification.

---

## Attack Classification Engine

The classifier auto-tags every honeypot hit into one of four attack types:

| Attack Type | Detection Method | Example |
|---|---|---|
| **SQL Injection** | Payload pattern matching | `' OR 1=1--`, `UNION SELECT` |
| **Brute Force** | Redis rate tracking per IP | 10+ requests in 60 seconds |
| **Scanner** | User-agent fingerprinting + endpoint diversity | `sqlmap`, `nikto`, 5+ endpoints in 30s |
| **Recon** | Default for all honeypot hits | Accessing `/config/env` |

Priority order: SQL Injection → Brute Force → Scanner → Recon

---

## Database Schema

```sql
-- Users table
users (id, username, password, balance, created_at)

-- Transactions table
transactions (id, sender_id, receiver_id, amount, timestamp)

-- Honeypot logs
attack_logs (id, ip_address, endpoint, payload, attack_type, user_agent, timestamp)
```

---

## Setup & Running

### Prerequisites
- Python 3.10+
- PostgreSQL
- Redis or Memurai (Windows)
- Node.js 18+

### 1. Clone the repo
```bash
git clone https://github.com/PhoenixKnight-in/HoneyPay.git
cd HoneyPay
```

### 2. Create PostgreSQL database
```sql
CREATE DATABASE honeypay;
```

### 3. Set up environment variables

Create `.env` inside both `payment_api/` and `honeypot/`:
```env
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/honeypay
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REDIS_HOST=localhost
REDIS_PORT=6379
```

### 4. Install Python dependencies
```bash
pip install -r payment_api/requirements.txt
pip install -r honeypot/requirements.txt
pip install requests colorama  # for attack scripts
```

### 5. Install dashboard dependencies
```bash
cd dashboard
npm install
```

### 6. Run all services

Open four terminals:

```bash
# Terminal 1 — Payment API
cd payment_api
uvicorn main:app --reload --port 8000

# Terminal 2 — Honeypot
cd honeypot
uvicorn main:app --reload --port 8001

# Terminal 3 — Dashboard
cd dashboard
npm start

# Terminal 4 — Run attack scripts (demo)
cd attack_scripts
python sql_injection.py
python brute_force.py
python recon.py
```

---

## Live Demo Flow (3 Minutes)

1. Open dashboard at `http://localhost:3000` — attack counter at zero
2. Run `python sql_injection.py` — watch SQL Injection entries appear in real time
3. Point to the classification: *"The system automatically identified these as SQL Injection attempts"*
4. Run `python brute_force.py` — Brute Force entries appear with orange badges
5. Show the rate limiter on the Payment API — requests get 429 after attempt 5
6. Run `python recon.py` — Recon entries populate across all 5 trap endpoints
7. Show the donut chart updating with live attack type distribution

---

## Work Split

| Person A(ME) | Person B |
|----|----|
| Payment API + Honeypot Service + Redis Rate Limiting | Attack Scripts + React Dashboard |

---

## What I Built (Person A)

Built a secure payment API (FastAPI + PostgreSQL) with Redis rate limiting, bcrypt password hashing, JWT authentication, input validation, and parameterized queries. Designed a parallel honeypot service with 5 deceptive endpoints that log and auto-classify attacker behavior into SQL Injection, Brute Force, Recon, and Scanner categories using a custom classification engine with Redis-backed rate tracking.

---

*Built for interview demos. Every attack is real. Every detection is live.*
