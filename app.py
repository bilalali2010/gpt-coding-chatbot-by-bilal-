# app.py
# Streamlit app that uses a free Hugging Face model (distilgpt2/gpt2)
# Save this file as app.py in your GitHub repo.

import streamlit as st
from transformers import pipeline

# -------------------------
# Settings & caching
# -------------------------
st.set_page_config(page_title="Free GPT Chat", page_icon="💬", layout="centered")

# Sidebar controls (user can pick model and generation settings)
st.sidebar.header("Settings")
model_choice = st.sidebar.selectbox("Model (smaller = faster)", ("distilgpt2", "gpt2"))
max_length = st.sidebar.slider("Max tokens (response length)", 50, 300, 150, step=10)
temperature = st.sidebar.slider("Temperature (creativity)", 0.1, 1.0, 0.7, step=0.05)
top_p = st.sidebar.slider("Top-p (nucleus sampling)", 0.1, 1.0, 0.9, step=0.05)
do_sample = st.sidebar.checkbox("Use sampling (do_sample)", value=True)

# Cache the loaded pipeline so it is reused across reruns
@st.cache_resource
def load_generator(model_name):
    # device=-1 forces CPU (Streamlit Cloud usually has no GPU)
    return pipeline("text-generation", model=model_name, device=-1)

# -------------------------
# UI: Title and load model
# -------------------------
st.title("💬 Free GPT Chat — Streamlit + Transformers")
st.write("A simple chat interface using a free Hugging Face model (no API key).")

with st.spinner(f"Loading model {model_choice} (may take 30–90s first time)..."):
    generator = load_generator(model_choice)

# -------------------------
# Chat session state
# -------------------------
if "messages" not in st.session_state:
    # messages is a list of dicts: {"role": "user"/"bot", "text": "..."}
    st.session_state.messages = []

def clear_chat():
    # Clear conversation
    st.session_state.messages = []

# Buttons in sidebar
st.sidebar.button("Clear chat", on_click=clear_chat)

# -------------------------
# Input area
# -------------------------
user_input = st.text_input("You:", key="input")

if st.button("Send") and user_input.strip():
    # Add user message to history
    st.session_state.messages.append({"role": "user", "text": user_input})

    # Generate a response
    with st.spinner("Generating reply..."):
        try:
            # Generator returns a list of dicts with 'generated_text'
            out = generator(
                user_input,
                max_length=max_length + len(user_input.split()),  # rough guard
                do_sample=do_sample,
                temperature=float(temperature),
                top_p=float(top_p),
                num_return_sequences=1
            )
            raw = out[0]["generated_text"]

            # The model often repeats the prompt at start; remove if present
            if raw.startswith(user_input):
                bot_text = raw[len(user_input):].strip()
            else:
                bot_text = raw.strip()

            # Append bot response
            st.session_state.messages.append({"role": "bot", "text": bot_text})

        except Exception as e:
            st.session_state.messages.append({"role": "bot", "text": f"Error generating: {e}"})

# -------------------------
# Display chat history
# -------------------------
# Show newest at bottom (like normal chat)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['text']}")
    else:
        st.markdown(f"**Bot:** {msg['text']}")
