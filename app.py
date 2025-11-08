import streamlit as st
import requests
import json

# -------------------------
# Streamlit config
# -------------------------
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 AI Chatbot")

# -------------------------
# Hugging Face API settings
# -------------------------
HF_TOKEN = st.secrets["HF_TOKEN"]
API_URL = "https://router.huggingface.co/hf-inference-chat"  # ✅ correct for chat
MODEL_ID = "meta-llama/Llama-3-8b-instruct"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

# -------------------------
# Chat memory
# -------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if st.button("🧹 Clear Chat"):
    st.session_state["messages"] = []
    st.rerun()

# Display chat history
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# -------------------------
# User input
# -------------------------
user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    payload = {
        "model": MODEL_ID,
        "messages": st.session_state["messages"],
        "max_new_tokens": 300,
        "temperature": 0.8
    }

    try:
        res = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        if res.status_code != 200:
            response = f"❌ API Error {res.status_code}: {res.text}"
        else:
            result = res.json()
            # Parse response
            if "error" in result:
                response = f"❌ API Error: {result['error']}"
            elif "generated_text" in result:
                response = result["generated_text"]
            elif "choices" in result:
                response = result["choices"][0]["message"]["content"]
            else:
                response = "⚠️ Unexpected response: " + str(result)
    except Exception as e:
        response = f"❌ Error: {e}"

    st.session_state["messages"].append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
