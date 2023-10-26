import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import yfinance as yf

# User input for the ticker symbol
user_ticker = input("Enter the ticker symbol: ")

# Fetch stock data
try:
    stock = yf.Ticker(user_ticker)
    company_name = stock.info['longName']
    data = stock.history(period="1y")
except:
    raise ValueError("Invalid ticker symbol. Please provide a valid ticker symbol.")

data['momentum'] = data['Close'].pct_change()

# Create figure and subplots
figure = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05, subplot_titles=(f"{company_name} Stock Price", "Momentum"))

# Add traces for stock price and momentum
figure.add_trace(go.Scatter(x=data.index, y=data['Close'], name='Close Price', line=dict(color='royalblue')), row=1, col=1)
figure.add_trace(go.Scatter(x=data.index, y=data['momentum'], name='Momentum', yaxis='y2', line=dict(color='darkorange')), row=2, col=1)

# Add buy and sell markers
figure.add_trace(go.Scatter(x=data.loc[data['momentum'] > 0].index, y=data.loc[data['momentum'] > 0]['Close'],
                            mode='markers', name='Buy', marker=dict(color='green', symbol='triangle-up')), row=1, col=1)
figure.add_trace(go.Scatter(x=data.loc[data['momentum'] < 0].index, y=data.loc[data['momentum'] < 0]['Close'],
                            mode='markers', name='Sell', marker=dict(color='red', symbol='triangle-down')), row=1, col=1)

# Update layout
figure.update_layout(title=f'Historical Stock Data for {company_name} ({user_ticker}) over the past year',
                     xaxis_title='Date',
                     yaxis_title='Price',
                     yaxis2_title='Momentum',
                     yaxis=dict(title='Price', domain=[0.6, 1], showgrid=False),
                     yaxis2=dict(title='Momentum', domain=[0, 0.4], showgrid=False),
                     height=800,
                     showlegend=True,
                     plot_bgcolor='rgba(0,0,0,0)')

# Show figure
figure.show()
