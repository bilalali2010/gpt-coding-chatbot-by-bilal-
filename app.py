import streamlit as st
import requests
import json

# -------------------------
# STREAMLIT APP CONFIG
# -------------------------
st.set_page_config(page_title="My Hugging Face Chatbot", page_icon="🤖")
st.title("🤖 AI Chatbot")
st.write("Ask me anything and I'll reply using my Hugging Face model.")

# -------------------------
# HUGGING FACE API
# -------------------------
HF_TOKEN = st.secrets["HF_TOKEN"]
API_URL = "https://api.huggingface.co/v1/chat/completions"
MODEL_ID = "meta-llama/Llama-3-8b-instruct"  # ✅ Stable Model

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

# -------------------------
# CHAT MEMORY
# -------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# -------------------------
# USER INPUT
# -------------------------
user_input = st.chat_input("Type your message here...")

if user_input:
    # Display and store user message
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    payload = {
        "model": MODEL_ID,
        "messages": st.session_state["messages"],
        "max_tokens": 300,
        "temperature": 0.8
    }

    try:
        res = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        result = res.json()
        response = result["choices"][0]["message"]["content"]
    except Exception as e:
        response = f"❌ Error: {e}"

    st.session_state["messages"].append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
