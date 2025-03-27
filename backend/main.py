import json
import time

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from models import ClientMessage, ServerResponse
from services import fetch_stock_data, fetch_stock_news
from utils import extract_json_from_text

load_dotenv()

app = FastAPI()

model = ChatOpenAI(model="gpt-4o")
tools = [fetch_stock_data, fetch_stock_news]

sys_prompt = (
    "You are an expert in stock market analysis. "
    "Your task is to answer questions about a particular stock. "
    "Try to be as informative as possible and provide detailed explanations. "
    "Make sure any dollar value starts with a '$' symbol, do not try to apply formatting on the numbers. "
    "Generate a response that avoids unintended Markdown formatting issues. Ensure that:"
    "1. Any special characters (such as underscores _, asterisks *, or backticks `) that could be misinterpreted by Markdown are properly escaped using a backslash (\)."
    "2. Avoid unnecessary Markdown syntax unless explicitly required."
    "3. Any dollar amount larger than 1 million should be formatted in millions (e.g. $1.5M)."
)

agent = create_react_agent(model, tools, prompt=sys_prompt)

@app.post("/answer", response_model=ServerResponse)
def answer_question(message: ClientMessage):
    """Answer questions about a given stock ticker."""
    start = time.time()
    response = agent.invoke({"messages": [("human", message.content)]})
    end = time.time()

    return ServerResponse(query=message.content, response=response["messages"][-1].content, time_taken=end-start)





