import os
import json
import requests
import pandas as pd
import streamlit as st

from typing import Optional
from dotenv import load_dotenv

from models import ChatMessage
from plotters.history import plot_stock_history

load_dotenv()

API_ENDPOINT = os.environ.get("API_ENDPOINT")

def set_wide_mode():
    st.set_page_config(layout="wide")

set_wide_mode()

if "messages" not in st.session_state:
    st.session_state.messages = []


def fetch_stock_history(ticker: str, period: str = "1y") -> dict:
    """Fetch historical stock data for a given ticker symbol."""
    response = requests.get(f"{API_ENDPOINT}/history", params={"ticker": ticker, "period": period}).json()
    return json.loads(response["history"])


def handle_stock_query():
    """Handle stock queries."""
    ticker = st.session_state.ticker
    period = "1y"

    with st.spinner("Fetching historical price data..."):
        historical_data = fetch_stock_history(ticker, period=period)
        df = pd.DataFrame(historical_data)

    with st.spinner("Compiling summary..."):
        response = requests.get(f"{API_ENDPOINT}/summary/{ticker}").json()
        summary = response["response"]

    st.markdown(f"### Stock: {ticker.upper()}")
    st.markdown(summary)

    # Create the chart
    st.plotly_chart(plot_stock_history(df, ticker), use_container_width=True)


with st.sidebar:
    st.markdown("## Stock Researcher")
    st.markdown("Your assistant to ask questions about the stock market.")

    st.text_input("Stock Ticker", key="ticker", on_change=handle_stock_query)


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

    