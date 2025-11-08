import streamlit as st
import requests
import json

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 AI Chatbot")

HF_TOKEN = st.secrets["HF_TOKEN"]
MODEL_ID = "mistralai/Mistral‑7B-Instruct‑v0.1"
API_URL = f"https://router.huggingface.co/{MODEL_ID}"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if st.button("🧹 Clear Chat"):
    st.session_state["messages"] = []
    st.rerun()

for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

user_input = st.chat_input("Type your message here…")

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    payload = {
        "inputs": st.session_state["messages"],
        "parameters": {"max_new_tokens": 300, "temperature": 0.8}
    }

    try:
        res = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        if res.status_code != 200:
            response = f"❌ API Error {res.status_code}: {res.text}"
        else:
            result = res.json()
            if "generated_text" in result:
                response = result["generated_text"]
            elif "error" in result:
                response = f"❌ API Error: {result['error']}"
            else:
                response = "⚠️ Unexpected response: " + str(result)
    except Exception as e:
        response = f"❌ Error: {e}"

    st.session_state["messages"].append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
