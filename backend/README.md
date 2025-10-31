# Backend - Support Agent

Install:
pip install -r requirements.txt

Run:
uvicorn app:app --reload --host 127.0.0.1 --port 8000

Health:
GET /health
POST /respond  { "message": "..." }
