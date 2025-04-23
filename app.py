import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv(override=True)

# Get OpenAI API key
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    st.error("OpenAI API Key not set in .env file.")
    st.stop()

# Initialize OpenAI client
openai = OpenAI(api_key=openai_api_key)
MODEL = "gpt-4o-mini"

# Define system message
system_message = (
    "You are a helpful assistant for an Airline called FlightAI. "
    "Give short, courteous answers, no more than 1 sentence. "
    "Always be accurate. If you don't know the answer, say so."
)

# Streamlit UI
st.title("✈️ FlightAI Assistant")
st.markdown("Ask any question about your flight, booking, or airline services.")

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# User input
user_input = st.chat_input("Ask me something...")

# Process input and generate response
if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})
    messages = [{"role": "system", "content": system_message}] + st.session_state.history

    try:
        response = openai.chat.completions.create(
            model=MODEL,
            messages=messages
        )
        reply = response.choices[0].message.content
        st.session_state.history.append({"role": "assistant", "content": reply})
    except Exception as e:
        reply = f"Error: {e}"
        st.session_state.history.append({"role": "assistant", "content": reply})

# Display chat messages
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

