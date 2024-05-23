# Imports
import time  # to simulate a real time data, time loop
import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development
import plotly.graph_objects as go  # candle stick plots
import random
import os
import yfinance as yf
from concurrent.futures import ThreadPoolExecutor
import math
from datetime import datetime


st.set_page_config(
    page_title="Trading Bot",
    page_icon="🤖",
    layout="wide",
)

@st.cache_data
def get_dataset(path) -> pd.DataFrame:
    if os.path.exists(path):
        df = pd.read_csv(path)
        return df
    else:
        print("Path:", path, "does not exist!")

@st.cache_data
def filter_dataset_date(df, start_date, end_date) -> pd.DataFrame:
    df = df[(pd.to_datetime(df["Date"]) >= pd.to_datetime(start_date)) & 
                        (pd.to_datetime(df["Date"]) <= pd.to_datetime(end_date))]
    return df

def get_current_portfolio_value(trading_bot_df, portfolio, cash_balance, date):
    portfolio_value = cash_balance  # Initialize portfolio value with cash balance

    if portfolio:
        for stock_symbol, quantity in portfolio.items():
            stock_data = trading_bot_df[(trading_bot_df['Ticker'] == stock_symbol) & (trading_bot_df['Date'] == date)]  # Filter the DataFrame for the specific stock on the given date

            if not stock_data.empty:
                close_price = stock_data.iloc[0]['Close']
                stock_value = close_price * quantity
                
                portfolio_value += stock_value  # Add the stock value to the overall portfolio value

    return portfolio_value

def update_portfolio(trading_bot_df, stock_portfolio, cash_balance, date, threshhold, only_one_of_each_stock, mode):
    '''
    This function dynamically adjusts a stock portfolio based on predictions and a specified threshhold,
    executing buy and sell transactions while ensuring available cash balance.
    '''
    df_filtered_by_date = trading_bot_df[trading_bot_df['Date'] == date]  # Filter DataFrame for the given date
    
    # Iterate over rows in the DataFrame
    for index, row in df_filtered_by_date.iterrows():
        ticker = row['Ticker']
        
        predictions = {
            'Buy': row['Prediction_0'],   # Buy
            'Sell': row['Prediction_1'],  # Sell
            'Hold': row['Prediction_2']   # Hold
        }

        max_prediction = max(predictions.values())  # Get max probability
        best_action = max(predictions, key=predictions.get)  # Get best action with highest probability

        # BUY1 MODE
        if mode == "buy1perDay":
            # Decide whether to buy, sell, or hold based on threshhold
            if best_action == "Buy" and max_prediction >= threshhold and cash_balance-row['Close'] > 0:
                if not only_one_of_each_stock and ticker in stock_portfolio:
                    stock_portfolio[ticker] += 1
                    cash_balance -= row['Close']  # Deduct the cost of the stock from cash balance
                elif ticker not in stock_portfolio:
                    stock_portfolio[ticker] = 1
                    cash_balance -= row['Close']  # Deduct the cost of the stock from cash balance

            elif best_action == "Sell" and max_prediction >= threshhold and ticker in stock_portfolio.keys():
                if ticker in stock_portfolio:
                    if stock_portfolio[ticker] == 1:
                        del stock_portfolio[ticker]
                        cash_balance += row['Close']  # Add the selling price to cash balance
                    else:
                        stock_portfolio[ticker] -= 1
                        cash_balance += row['Close']  # Add the selling price to cash balance

        # SELL_FRIDAY MODE
        elif mode == "buybyBudget_SellFriday":
            # Decide whether to buy, sell, or hold based on threshhold
            if best_action == "Buy" and max_prediction >= threshhold and cash_balance-row['Close'] > 0:
                if ticker in stock_portfolio:
                    budget = cash_balance / availablePerDay  # bot uses 1/3 of cash balance to buy a stock
                    stock_amount = math.floor(budget // row['Close'])
                    stock_portfolio[ticker] += stock_amount
                    cash_balance -= stock_amount * row['Close']  # Deduct the cost of the stock from cash balance
                else:
                    budget = cash_balance / availablePerDay
                    stock_amount = math.floor(budget // row['Close'])
                    stock_portfolio[ticker] = stock_amount
                    cash_balance -= stock_amount * row['Close']   

            conv_date =  datetime.strptime(date, '%Y-%m-%d')
            if conv_date.weekday() == 4:
                if ticker in stock_portfolio:
                    cash_balance += row['Close']*stock_portfolio[ticker]  # Add the selling price to cash balance
                    del stock_portfolio[ticker]
        
    return stock_portfolio, cash_balance


########### Start of Gui ###########

sp500_df = get_dataset(path = '../CNN/test_data/^GSPC.csv')
v1 = get_dataset(path = 'predicted_data/predicted_data_V1.csv')
v2 = get_dataset(path = 'predicted_data/predicted_data_V2.csv')
v3 = get_dataset(path = 'predicted_data/predicted_data_V3.csv')


# dashboard title
st.title("Trading Bot Dashboard 💸")

# Dropdown for selecting the algo
algo = st.selectbox("Select trading Algo", options=["V1_noSMOTE", "V2_withSMOTE", "V3_withSMOTE"])

if algo == "V1_noSMOTE":
    trading_bot_df = v1
elif algo == "V2_withSMOTE":
    trading_bot_df = v2
elif algo == "V3_withSMOTE":
    trading_bot_df = v3

# Determine min and max dates from the DataFrame
min_date = pd.to_datetime(sp500_df['Date']).min()
max_date = pd.to_datetime(sp500_df['Date']).max()

# Date range filters
date_filter_col1, date_filter_col2 = st.columns(2)
start_date = date_filter_col1.date_input("Select start date", value=min_date, min_value=min_date, max_value=max_date)
end_date = date_filter_col2.date_input("Select end date", value=max_date, min_value=min_date, max_value=max_date)

error_placeholder = st.empty()

bot_settings_col1, bot_settings_col2 = st.columns(2)
# starting cash balance
starting_balance = bot_settings_col1.number_input("Select a starting balance ($)", min_value=1000, max_value=1000000)

# tick rate
tick_rate = bot_settings_col2.number_input("Select tickrate (seconds)", min_value=0.2, max_value=1.0, step=0.1, value=0.4)

st.markdown("---")

control_col1, control_col2 = st.columns(2)
button_col1, button_col2 = control_col1.columns(2)

# Bot start button
bot_start = button_col1.button("Start / Restart Trading Bot")
# Bot stop button
bot_stop = button_col2.button("Stop")

settings_col1, settings_col2 = control_col2.columns(2)
# Risk threshhold
risk_threshhold = settings_col1.slider(label="Risk Threshhold", max_value=1.0, min_value=0.34, step=0.01, value=0.75)
settings_col1.text("Risk Threshhold = minimum CNN prediction\nprobability required\nto execute a trade.")
settings_col2.markdown("")
settings_col2.markdown("")
mode = settings_col2.selectbox("Select trading mode", options=["buy1perDay", "buybyBudget_SellFriday"])
only_one_of_each_stock = False
if mode == "buy1perDay":
    settings_col2.markdown("")
    settings_col2.markdown("")
    only_one_of_each_stock = settings_col2.checkbox(label="Trading Bot should hold maximum 1 of each stock")

elif mode == "buybyBudget_SellFriday":
    availablePerDay = settings_col2.number_input("Available budget per day in percent", min_value=1, max_value=10, value=3)


# creating a single-element container
plots_placeholder = st.empty()

if bot_start and (start_date < end_date):
    sp500_filtered_df = filter_dataset_date(sp500_df, start_date, end_date)
    trading_bot_filtered_df = filter_dataset_date(trading_bot_df, start_date, end_date)
    
    # Initialization of all important variables
    portfolio_value_list = []  # List with portfolio value per tick
    cash_balance_list = []  # List with cash balance per tick
    ticks = 1  # Variable to filter dataframes (every iteration: ticks += 1)
    stock_portfolio = {}  # stock portfolio: key = ticker, value = quantity
    cash_balance = starting_balance  # initialize cash balance with starting balance
    dates = sp500_filtered_df['Date'].to_list()  # List of dates for plotting and looping

    # near real-time / live feed simulation
    for current_date in dates:
        
        if bot_stop:
            break

        sp500_stream_df = sp500_filtered_df.iloc[:ticks]

        cash_balance_list.append(cash_balance)

        ##### GET CURRENT BALANCE #####
        # portfolio_value_list = stocks + cash
        portfolio_value_list.append(get_current_portfolio_value(trading_bot_df, stock_portfolio, cash_balance, date=current_date))  # calculate balance (current porfolio value)

        with plots_placeholder.container():
            
            st.markdown("---")

            # create two columns for charts
            fig_col1, fig_col2 = st.columns(2)
            with fig_col1:
                candlestick_fig = go.Figure(data=[go.Candlestick(x=sp500_stream_df['Date'],
                                                                open=sp500_stream_df['Open'],
                                                                high=sp500_stream_df['High'],
                                                                low=sp500_stream_df['Low'],
                                                                close=sp500_stream_df['Close'])])

                candlestick_fig.update_layout(title="S&P 500 Candlestick Chart",
                                            xaxis_title="Date",
                                            yaxis_title="Price (USD)")
                
                # Disable draggable date filter
                candlestick_fig.update_xaxes(
                    rangeslider_visible=False,
                    rangebreaks=[
                        dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
                    ]
                )
                st.plotly_chart(candlestick_fig)

                portfolio_fig = go.Figure(data=[go.Pie(labels=list(stock_portfolio.keys()), values=list(stock_portfolio.values()))])
                portfolio_fig.update_layout(
                    title="Stock Portfolio Distribution (Quantity per stock)"
                )
                if len(stock_portfolio.keys())<20:
                    portfolio_fig.update_traces(
                        textinfo='label'
                    )
                st.plotly_chart(portfolio_fig)

            with fig_col2:
                if portfolio_value_list[-1] < starting_balance:
                    color="red"
                else:
                    color="green"

                balance_fig = px.line(
                    x = dates[:ticks],
                    y = portfolio_value_list[:ticks],
                    color_discrete_sequence=[color]
                )

                balance_fig.update_layout(title="Balance of Trading bot (Cash + Stocks values)",
                            xaxis_title="Date",
                            yaxis_title="Balance (USD)"
                            )

                st.plotly_chart(balance_fig)

                if len(portfolio_value_list) > 1:
                    st.metric(
                        label="Cash balance",
                        value="${:.2f}".format(cash_balance_list[-1]),
                        delta=round(cash_balance_list[-1]-cash_balance_list[-2], 2)
                    )

                    st.metric(
                        label="Stocks value",
                        value="${:.2f}".format(portfolio_value_list[-1] - cash_balance_list[-1]),
                        delta=round((portfolio_value_list[-1]-cash_balance_list[-1])-(portfolio_value_list[-2]-cash_balance_list[-2]), 2)
                    )

                    st.metric(
                        label="Total Balance",
                        value="${:.2f}".format(portfolio_value_list[-1]),
                        delta=round(portfolio_value_list[-1]-portfolio_value_list[-2], 2)
                    )

                    st.metric(
                        label="Index Performance",
                        value="{:.2f} %".format(sp500_stream_df['Close'].iloc[-1]/(sp500_stream_df['Close'].iloc[0])*100-100)
                    )

                    st.metric(
                        label="Bot Performance",
                        value="{:.2f} %".format(portfolio_value_list[-1]/(portfolio_value_list[0])*100-100)
                    )

            ##### UPDATE PORTFOLIO #####
            stock_portfolio, cash_balance = update_portfolio(trading_bot_df, stock_portfolio, cash_balance, date=current_date, threshhold=risk_threshhold, only_one_of_each_stock=only_one_of_each_stock, mode=mode)  # Get updated portfolio based on current date
            
            ticks += 1
            time.sleep(tick_rate)

elif end_date < start_date:
    error_placeholder.error("End date cannot be before start date.")

st.markdown("---")