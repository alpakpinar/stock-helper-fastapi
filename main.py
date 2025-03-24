import json

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from models import StockMetricsResponseModel, StockNewsResponseModel, NewsArticle
from services import fetch_stock_data, summarize_stock_data, fetch_stock_news, summarize_news
from utils import extract_json_from_text

load_dotenv()

app = FastAPI()

@app.get("/metrics/{ticker}", response_model=StockMetricsResponseModel)
def get_stock_data(ticker: str):
    """Get stock data for a given ticker and respond to client with the summary of the data."""
    # Get the data for the ticker using Yahoo Finance API
    stock_data = fetch_stock_data(ticker)

    if not stock_data:
        return HTTPException(status_code=404, detail=f"Stock {ticker} is not found.")
    
    summary = summarize_stock_data(stock_data)

    return StockMetricsResponseModel(summary=summary, stock_ticker=stock_data["symbol"])


@app.get("/news/{ticker}", response_model=StockNewsResponseModel)
def get_stock_news(ticker: str):
    """Get stock news for a given ticker and respond to client with the summary of the news."""
    stock_news = fetch_stock_news(ticker, num_articles_max=5)

    if not stock_news:
        return HTTPException(status_code=404, detail=f"No news articles are found for stock {ticker}.")

    processed_articles = []

    for article in stock_news:
        raw = summarize_news(article)
        response = extract_json_from_text(raw)
        if not response:
            continue

        processed_articles.append(
            NewsArticle(
                title=article["content"]["title"],
                url=article["content"]["clickThroughUrl"]["url"],
                summary=response["summary"],
                sentiment=response["sentiment"]
            )
        )

    
    return StockNewsResponseModel(stock_ticker=ticker, articles=processed_articles)



