from pydantic import BaseModel
from typing import Optional


class ClientMessage(BaseModel):
    """Model for client messages."""
    query: str
    context: Optional[str] = None


class ServerResponse(BaseModel):
    """Model for server responses."""
    query: str
    response: str
    time_taken: float


class PriceHistoryResponse(BaseModel):
    """Model for price history responses."""
    period: str
    ticker: str
    history: str
