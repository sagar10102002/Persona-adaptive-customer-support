# Persona-adaptive-customer-support
# Support Agent (frontend + backend)

Start backend:
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --host 127.0.0.1 --port 8000

Start frontend (another terminal):
cd frontend
pip install -r requirements.txt
streamlit run streamlit_app.py

Open UI: http://localhost:8501 (Streamlit)
Check backend docs: http://127.0.0.1:8000/docs
