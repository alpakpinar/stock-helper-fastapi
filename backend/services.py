import yfinance

from langchain_core.tools import tool


@tool
def fetch_stock_data(ticker: str) -> dict:
    """Fetch stock data from Yahoo Finance API for a given ticker symbol."""
    raw = yfinance.Ticker(ticker).info

    keys_to_extract = [
        "symbol",
        "trailingEps",
        "forwardEps",
        "lastDividendValue",
        "lastDividendDate",
        "fiftyTwoWeekLow",
        "fiftyTwoWeekHigh",
        "52WeekChange",
        "currentPrice",
        "targetHighPrice",
        "targetLowPrice",
        "targetMeanPrice",
        "targetMedianPrice",
        "totalRevenue",
        "revenuePerShare",
        "dividendYield",
        "marketCap",
        "recommendationMean",
        "recommendationKey",
    ]

    res = {key: raw[key] for key in keys_to_extract if key in raw}
    
    return res


@tool
def fetch_stock_news(ticker: str, num_articles_max: int = 5) -> list:
    """Fetch stock news from Yahoo Finance API for a given ticker symbol."""
    return yfinance.Ticker(ticker).news[:num_articles_max]


def fetch_history(ticker: str, period: str = "1y") -> str:
    """Fetch historical stock data from Yahoo Finance API for a given ticker symbol."""
    return yfinance.Ticker(ticker).history(period=period).reset_index().to_json(orient="records", date_format="iso")


if __name__ == "__main__":
    data = fetch_history("AAPL", period="10d").reset_index().to_json(orient="records", date_format="iso")
    print(data)
