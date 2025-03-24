from pydantic import BaseModel
from typing import List


class StockMetricsResponseModel(BaseModel):
    """Response model for stock metric queries."""
    summary: str
    stock_ticker: str


class NewsArticle(BaseModel):
    """Model for a single news article."""
    title: str
    url: str
    summary: str
    sentiment: str


class StockNewsResponseModel(BaseModel):
    """Response model for stock news queries."""
    stock_ticker: str
    articles: List[NewsArticle]