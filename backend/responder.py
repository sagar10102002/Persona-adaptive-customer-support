import os, json, requests
from dotenv import load_dotenv
from utils.persona import detect_persona
from responder import generate_response

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.1-70b-instruct")
OPENROUTER_API_URL = os.getenv("OPENROUTER_API_URL", "https://openrouter.ai/api/v1/chat/completions")

# Load knowledge base
KB_PATH = os.path.join(os.path.dirname(__file__), "kb/knowledge_base.json")
with open(KB_PATH, "r") as f:
    KNOWLEDGE_BASE = json.load(f)

def retrieve_kb_content(message: str) -> str:
    for key, value in KNOWLEDGE_BASE.items():
        if key in message.lower():
            return value
    return None

def generate_response(message: str) -> str:
    print(f"🔹 Received message: {message}")

    try:
        persona = detect_persona(message)
        print(f"🧠 Detected persona: {persona}")

        kb_content = retrieve_kb_content(message)
        print(f"📘 KB Content: {kb_content if kb_content else 'None found'}")

        # Tone & intent based on persona
        tone_prompt = {
            "technical expert": "Provide a concise and technical explanation.",
            "frustrated user": "Be empathetic, reassuring, and friendly.",
            "business exec": "Be professional, brief, and focused on ROI/value.",
            "general user": "Be clear and approachable."
        }[persona]

        # Escalation logic
        escalate = "urgent" in message.lower() or "not working" in message.lower()

        system_prompt = f"""
You are an AI support assistant.
User persona: {persona}.
Tone guideline: {tone_prompt}
{"If issue seems severe or unresolved, recommend escalation to human support with context summary." if escalate else ""}
"""

        user_prompt = message
        if kb_content:
            user_prompt += f"\nRelevant Knowledge Base Info: {kb_content}"

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }

        data = {
            "model": OPENROUTER_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt.strip()},
                {"role": "user", "content": user_prompt.strip()}
            ],
            "temperature": 0.7
        }

        response = requests.post(OPENROUTER_API_URL, headers=headers, json=data, timeout=60)

        if response.status_code == 200:
            result = response.json()
            reply = result["choices"][0]["message"]["content"]
            if escalate:
                reply += "\n\n🚨 Escalation suggested: Forward conversation and user context to Tier-2 support."
            return reply
        else:
            print("❌ API Error:", response.text)
            return "Sorry, I encountered a problem processing your request."

    except Exception as e:
        print("❌ Exception:", e)
        return "Sorry, there was an issue generating the response."
