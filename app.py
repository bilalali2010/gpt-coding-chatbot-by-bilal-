import streamlit as st
import requests
import json

# -------------------------
# STREAMLIT APP CONFIG
# -------------------------
st.set_page_config(page_title="My Hugging Face Chatbot", page_icon="🤖")
st.title("🤖 AI Chatbot")
st.write("Ask me anything and I will reply using my Hugging Face model!")

# -------------------------
# HUGGING FACE API SETTINGS
# -------------------------
HF_TOKEN = st.secrets["HF_TOKEN"]
API_URL = "https://api-inference.huggingface.co/v1/chat/completions"
MODEL_ID = "meta-llama/Llama-3-8b-instruct"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

# -------------------------
# CHAT MEMORY
# -------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []


# Button to clear chat
# Button to clear chat
if st.button("🧹 Clear Chat"):
    st.session_state["messages"] = []
    st.rerun()


# Display conversation history
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# -------------------------
# USER INPUT
# -------------------------
user_input = st.chat_input("Type your message here...")

if user_input:
    # Show user message
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    payload = {
        "model": MODEL_ID,
        "messages": st.session_state["messages"],
        "max_tokens": 300,
        "temperature": 0.8,
        "stream": False
    }

    try:
        res = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        result = res.json()

        # Handling multiple possible response formats ✅
        if "choices" in result:
            response = result["choices"][0]["message"]["content"]
        elif "generated_text" in result:
            response = result["generated_text"]
        else:
            response = "⚠️ Unexpected response: " + str(result)

    except Exception as e:
        response = f"❌ Error: {e}"

    # Display assistant message
    st.session_state["messages"].append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
