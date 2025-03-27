from pydantic import BaseModel
from typing import List


class ClientMessage(BaseModel):
    """Model for client messages."""
    content: str


class ServerResponse(BaseModel):
    """Model for server responses."""
    query: str
    response: str
    time_taken: float
