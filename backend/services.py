import yfinance
from openai import OpenAI


def fetch_stock_data(ticker: str) -> dict:
    """Fetch stock data from Yahoo Finance API."""
    raw = yfinance.Ticker(ticker).info

    keys_to_extract = [
        "symbol",
        "trailingEps",
        "forwardEps",
        "lastDividendValue",
        "lastDividendDate",
        "fiftyTwoWeekLow",
        "fiftyTwoWeekHigh",
        "fiftyDayAverage",
        "twoHundredDayAverage",
        "sharesOutstanding",
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


def fetch_stock_news(ticker: str, num_articles_max: int = 5) -> list:
    """Fetch stock news from Yahoo Finance API."""
    return yfinance.Ticker(ticker).news[:num_articles_max]


def summarize_stock_data(stock_data: dict) -> str:
    """Summarize stock data."""
    sys_prompt = (
        "You are an expert in stock market analysis. "
        "You will be given some stock data in JSON format, your task is to summarize the data. "
        "Please use the following format: '<stock ticker> is currently trading at $<current price>. It has a target median price of $<target median price>, which represents x\% of upside/downside. "
        "Financial metrics are as follows: <financial metrics in list format>'. "
        "When listing financial metrics, try to group them together based on their type. For example, you can group earnings per share metrics together, revenue metrics together, target price and buy/sell recommendations together etc. "
        "Please format any dollar values properly, starting with a $ symbol. "
        "Generate a response that avoids unintended Markdown formatting issues. Ensure that:"
        "1. Any special characters (such as underscores _, asterisks *, or backticks `) that could be misinterpreted by Markdown are properly escaped using a backslash (\)."
        "2. Avoid unnecessary Markdown syntax unless explicitly required."
        "3. Any dollar amount larger than 1 million should be formatted in millions (e.g. $1.5M)."
        "At the very end of your response, try to provide a few sentences of recommendation based on the data. "
    )

    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": sys_prompt
            },
            {
                "role": "user",
                "content": f"Here is the stock data: {stock_data}"
            }
        ]
    )

    return completion.choices[0].message.content


def summarize_news(article: dict) -> str:
    """Summarize stock news."""
    sys_prompt = (
        "You are an expert in stock market analysis. "
        "You will be given a news article about a particular stock. Your task is to do two things: "
        "1. Provide a brief summary of the news article (in a few sentences). "
        "2. Analyze the sentiment of the news article, is it Bullish, Bearish or Neutral? "
        "You can also provide some insights or recommendations based on the news. "
        "You must respond with the following JSON format: "
        '{"summary": "Brief summary of the article", "sentiment": "Bullish/Bearish/Neutral"} '
        "Do NOT wrap your response with backticks or any other formatting. "
    )

    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": sys_prompt
            },
            {
                "role": "user",
                "content": f"Article: {article['content']['summary']}"
            }
        ]
    )

    return completion.choices[0].message.content


if __name__ == "__main__":
    res = fetch_stock_news("AAPL")[0]
    from pprint import pprint
    pprint(res)