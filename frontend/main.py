import os
import requests
import streamlit as st

from typing import Optional
from dotenv import load_dotenv

from models import ChatMessage

load_dotenv()

API_ENDPOINT = os.environ.get("API_ENDPOINT")

def set_wide_mode():
    st.set_page_config(layout="wide")

set_wide_mode()

if "messages" not in st.session_state:
    st.session_state.messages = []


with st.sidebar:
    st.markdown("## Stock Researcher")
    st.markdown("Get stock metrics and news for a given ticker.")

def display_message(message: ChatMessage):
    """Display a chat message."""
    with st.chat_message(message.role):
        st.markdown(message.content)

        if message.caption is not None:
            st.caption(message.caption)


def handle_user_input(prompt: str):
    user_msg = ChatMessage(role="user", content=prompt)

    display_message(user_msg)
    st.session_state.messages.append(user_msg)

    with st.spinner("Analyzing..."):
        response = requests.post(f"{API_ENDPOINT}/answer", json={"content": prompt}).json()
        assistant_msg = ChatMessage(role="assistant", content=response["response"], caption=f"Time taken: {response['time_taken']:.3f} seconds")

        display_message(assistant_msg)
        st.session_state.messages.append(assistant_msg)

for message in st.session_state.messages:
    display_message(message)

if prompt := st.chat_input("What would you like to ask?"):
    handle_user_input(prompt)

    