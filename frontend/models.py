from dataclasses import dataclass
from typing import Optional


@dataclass
class ChatMessage:
    role: str
    content: str
    caption: Optional[str] = None


@dataclass
class StockOverview:
    symbol: str
    ai_summary: str
    historical_data: str