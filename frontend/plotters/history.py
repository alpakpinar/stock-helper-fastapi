import pandas as pd
import plotly.graph_objects as go

def plot_stock_history(df: pd.DataFrame, ticker: str) -> go.Figure:
    # Nothing to plot
    if df.empty:
        return
    
    latest_price = df['Close'].iloc[-1]
    first_price = df['Close'].iloc[0]
    percent_change = ((latest_price - first_price) / first_price) * 100

    fig = go.Figure()
    
    # Add vertical hover line
    fig.add_trace(go.Scatter(
        x=df['Date'], y=df['Close'],
        mode='lines',
        hoverinfo='x+y',
        showlegend=False
    ))
    
    # Add latest price and % change annotation
    fig.add_annotation(
        x=df['Date'].iloc[0],
        y=max(df['Close']),
        text=f"Price: ${latest_price:.2f} ({percent_change:.2f}%)",
        showarrow=False,
        align='left',
        bgcolor='white',
        bordercolor='black',
        borderwidth=1
    )
    
    fig.update_layout(
        title=f"{ticker} Stock Price History",
        xaxis_title="Date",
        yaxis_title="Stock Price ($)",
        hovermode='x unified'
    )

    return fig