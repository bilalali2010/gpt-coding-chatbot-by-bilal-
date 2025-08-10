import streamlit as st
from huggingface_hub import InferenceClient

# -------------------------
# STREAMLIT APP CONFIG
# -------------------------
st.set_page_config(page_title="My Hugging Face Chatbot", page_icon="🤖")

st.title("🤖 AI Chatbot")
st.write("Ask me anything and I'll reply using my Hugging Face model.")

# -------------------------
# HUGGING FACE CLIENT
# -------------------------
HF_TOKEN = st.secrets["HF_TOKEN"]  # Make sure you added this in Streamlit Secrets
MODEL_ID = "gpt2"  # Change to your model name on Hugging Face

client = InferenceClient(model=mistralai/Mistral-7B-Instruct-v0.3, token=HF_TOKEN)

# -------------------------
# CHAT MEMORY
# -------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# -------------------------
# USER INPUT
# -------------------------
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message to history
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Get AI response
    try:
        response = client.text_generation(user_input, max_new_tokens=200)
    except Exception as e:
        response = f"❌ Error: {e}"

    # Add AI response to history
    st.session_state["messages"].append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
