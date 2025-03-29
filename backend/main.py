import json
import time

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from models import ClientMessage, ServerResponse, PriceHistoryResponse
from services import fetch_stock_data, fetch_stock_news, fetch_history
from prompts import Prompt

load_dotenv()

app = FastAPI()

model = ChatOpenAI(model="gpt-4o")
tools = [fetch_stock_data, fetch_stock_news, fetch_history]


@app.post("/answer", response_model=ServerResponse)
def answer_question(message: ClientMessage):
    """Answer questions about a given stock ticker."""
    start = time.time()
    agent = create_react_agent(model, tools, prompt=Prompt.QA_BOT)
    
    try:
        response = agent.invoke({"messages": [("human", message.content)]})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    end = time.time()

    return ServerResponse(query=message.content, response=response["messages"][-1].content, time_taken=end-start)


@app.get("/summary/{ticker}", response_model=ServerResponse)
def get_stock_summary(ticker: str):
    """Return an LLM-generated summary for the given stock."""
    start = time.time()
    agent = create_react_agent(model, tools, prompt=Prompt.SUMMARIZER_BOT)

    try:
        prompt = f"Can you provide a summary of {ticker}?"
        response = agent.invoke({"messages": [("human", prompt)]})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    end = time.time()
    return ServerResponse(query=ticker, response=response["messages"][-1].content, time_taken=end-start)


@app.get("/history", response_model=PriceHistoryResponse)
def get_stock_history(ticker: str, period: str = "1y"):
    """Fetch historical stock data for a given ticker symbol."""
    try:
        data = fetch_history(ticker, period)
        return PriceHistoryResponse(period=period, ticker=ticker, history=data)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))




