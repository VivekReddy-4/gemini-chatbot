import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Streamlit page setup
st.set_page_config(
    page_title="Chat with Gemini",
    page_icon='🧠',
    layout="centered"
)

# Get API key and configure
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("❌ GOOGLE_API_KEY not found. Check your .env file!")
    st.stop()

gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel("gemini-2.0-flash")

# Session state setup
def map_role(role):
    return "assistant" if role == "model" else role

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# App title
st.title("Generative AI Chatbot")

# Display chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(map_role(message.role)):
        st.markdown(message.parts[0].text)

# Input from user
user_input = st.chat_input("Type your query here...")

if user_input:
    st.chat_message("user").markdown(user_input)
    response = st.session_state.chat_session.send_message(user_input)

    with st.chat_message("assistant"):
        st.markdown(response.text)
