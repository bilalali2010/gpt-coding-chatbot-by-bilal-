import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(page_title="My HF Chatbot", page_icon="🤖")
st.title("🤖 AI Chatbot")

HF_TOKEN = st.secrets["HF_TOKEN"]  # Make sure your token is here

MODEL_ID = "meta-llama/Llama-3-8b-instruct"
client = InferenceClient(model=MODEL_ID, token=HF_TOKEN)

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Clear chat button
if st.button("🧹 Clear Chat"):
    st.session_state["messages"] = []
    st.rerun()

# Display chat history
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# Get user input
user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # call the model
    try:
        completion = client.chat_completion(
            messages=st.session_state["messages"],
            max_tokens=300,
            temperature=0.8
        )
        response = completion.choices[0].message["content"]
    except Exception as e:
        response = f"❌ Error: {e}"

    st.session_state["messages"].append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
