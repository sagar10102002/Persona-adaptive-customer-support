import streamlit as st
import requests
import json
from datetime import datetime, timezone

API_URL = "http://127.0.0.1:8000/respond"

st.set_page_config(page_title="AI Support Agent", page_icon="🤖", layout="wide")

st.title("🤖 AI Support Agent")
st.markdown("### Smart assistant that detects persona, adapts tone, and resolves issues.")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.chat_input("Type your question...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("Analyzing your message..."):
        try:
            res = requests.post(API_URL, json={"message": user_input})
            if res.status_code == 200:
                bot_reply = res.json().get("response", "No response received.")
            else:
                bot_reply = f"⚠️ Error {res.status_code}: Backend issue."
        except Exception as e:
            bot_reply = f"Error: {str(e)}"
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

st.markdown("---")
st.caption(f"Last updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
