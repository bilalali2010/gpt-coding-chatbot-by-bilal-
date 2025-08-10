import streamlit as st
import requests
import os

# Hugging Face API Config
API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
headers = {"Authorization": f"Bearer {os.environ['HF_API_KEY']}"}

# Function to send text to Hugging Face Inference API
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Streamlit UI
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("💬 AI Sentiment Chatbot")

# Chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Input from user
user_input = st.text_input("You:", "")

# When user sends a message
if st.button("Send"):
    if user_input.strip():
        # Add user message
        st.session_state["messages"].append({"role": "user", "content": user_input})

        # Get AI response from Hugging Face
        output = query({"inputs": user_input})

        # Extract label + score
        try:
            label = output[0]['label']
            score = round(output[0]['score'], 2)
            ai_reply = f"Sentiment: **{label}** (Confidence: {score})"
        except:
            ai_reply = "Error getting sentiment."

        # Add AI reply
        st.session_state["messages"].append({"role": "assistant", "content": ai_reply})

# Display conversation
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**AI:** {msg['content']}")

