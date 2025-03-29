import os
import json
import requests
import pandas as pd
import streamlit as st

from typing import Optional
from dotenv import load_dotenv

from models import ChatMessage, StockOverview
from plotters.history import plot_stock_history

load_dotenv()

API_ENDPOINT = os.environ.get("API_ENDPOINT")

def set_wide_mode():
    st.set_page_config(layout="wide")

set_wide_mode()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "stock_overviews" not in st.session_state:
    st.session_state.stock_overviews = []


def fetch_stock_history(ticker: str, period: str = "1y") -> dict:
    """Fetch historical stock data for a given ticker symbol."""
    response = requests.get(f"{API_ENDPOINT}/history", params={"ticker": ticker, "period": period}).json()
    return json.loads(response["history"])


def handle_stock_query():
    """Handle stock queries."""
    ticker = st.session_state.ticker
    period = "1y"

    with st.status(f"Searching data for {ticker}...", expanded=True) as status:
        st.write("Fetching historical price data.")
        historical_data = fetch_stock_history(ticker, period=period)
        df = pd.DataFrame(historical_data)
        
        
        st.write("Compiling summary of metrics and news.")
        response = requests.get(f"{API_ENDPOINT}/summary/{ticker}").json()
        summary = response["response"]
        
        status.update(
            label="Done!", state="complete", expanded=False
        )

    overview = StockOverview(symbol=ticker, ai_summary=summary, historical_data=df.to_json())

    st.session_state.stock_overviews.append(overview)


with st.sidebar:
    st.markdown("## Stock Researcher")
    st.markdown("Your assistant to ask questions about the stock market.")

    st.text_input("Stock Ticker", key="ticker", on_change=handle_stock_query)


def display_stock_overview(overview: StockOverview):
    """Display a stock overview."""
    st.markdown(f"### Stock: {overview.symbol.upper()}")
    st.markdown(overview.ai_summary)

    df = pd.DataFrame(json.loads(overview.historical_data))
    st.plotly_chart(plot_stock_history(df, overview.symbol), use_container_width=True)


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
        context_builder = []
        for stock_overview in st.session_state.stock_overviews:
            context_builder.append(stock_overview.ai_summary)
        
        payload = {"query": prompt}

        if context_builder:
            payload["context"] = " ".join(context_builder)

        response = requests.post(f"{API_ENDPOINT}/answer", json=payload).json()
        assistant_msg = ChatMessage(role="assistant", content=response["response"], caption=f"Time taken: {response['time_taken']:.3f} seconds")

        display_message(assistant_msg)
        st.session_state.messages.append(assistant_msg)

for overview in st.session_state.stock_overviews:
    display_stock_overview(overview)

for message in st.session_state.messages:
    display_message(message)

if prompt := st.chat_input("What would you like to ask?"):
    handle_user_input(prompt)

    