# Event Management Platform (DevSecOps Demo)

A minimal full-stack Event Management Platform intentionally seeded with
**controlled OWASP vulnerabilities** for CI/CD security-scanning demonstrations
(SonarQube, Bandit, OWASP Dependency Check, pip-audit, Trivy, npm audit, etc.).

> ⚠️ **DO NOT DEPLOY TO PRODUCTION.**
> This codebase contains intentional vulnerabilities used to demonstrate
> DevSecOps scanning and remediation workflows.

## Structure

```
event-management-platform/
├── client/    # React + Vite + Tailwind + React Router + Axios
└── server/    # Python + Flask + SQLAlchemy + SQLite + JWT
```

Each folder is self-contained and can be pushed to its own GitHub repo.

## Quick start (Docker)

```bash
docker-compose up --build
```

- Frontend: http://localhost:5173
- Backend:  http://localhost:5000

## Quick start (local)

Backend:
```bash
cd server
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Frontend:
```bash
cd client
npm install
npm run dev
```

## Default admin

Seeded on first run:

- email: `admin@example.com`
- password: `Admin@123`

## Intentional Vulnerabilities (initial version)

| OWASP | Where | Notes |
|-------|-------|-------|
| A01 – Broken Access Control | `server/routes/admin_routes.py` | Admin endpoints skip role checks |
| A03 – SQL Injection | `server/controllers/event_controller.py` `search_events` | Raw string-concatenated SQL |
| A05 – Security Misconfiguration | `server/app.py`, `server/config.py` | `debug=True`, `CORS(*)`, verbose errors, hardcoded secret |
| A06 – Vulnerable Components | `server/requirements.txt` | Outdated Flask, Werkzeug, Jinja2, requests, PyYAML |

Each vulnerability is isolated so a "fix" branch can remediate cleanly (see
comments marked `# VULN:` and `# FIX:` in source).

## Scanning

```bash
# Python
pip install bandit pip-audit
bandit -r server
pip-audit -r server/requirements.txt

# Node
cd client && npm audit

# Container
trivy fs .
```
