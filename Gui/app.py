'''
- src: https://blog.streamlit.io/how-to-build-a-real-time-live-dashboard-with-streamlit/
'''

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


st.set_page_config(
    page_title="Trading Bot",
    page_icon="🤖",
    layout="wide",
)

@st.cache_data
def get_sp500_dataset(path = '../CNN/test_data/^GSPC.csv') -> pd.DataFrame:
    if os.path.exists(path):
        df = pd.read_csv(path)
        return df
    else:
        print("Path:", path, "does not exist!")

@st.cache_data
def filter_sp500_dataset(df, start_date, end_date):
    df = df[(pd.to_datetime(df["Date"]) >= pd.to_datetime(start_date)) & 
                        (pd.to_datetime(df["Date"]) <= pd.to_datetime(end_date))]
    return df

sp500_df = get_sp500_dataset()

# dashboard title
st.title("Trading Bot Dashboard")

# Determine min and max dates from the DataFrame
min_date = pd.to_datetime(sp500_df['Date']).min()
max_date = pd.to_datetime(sp500_df['Date']).max()

# Date range filters
date_filter_col1, date_filter_col2 = st.columns(2)
start_date = date_filter_col1.date_input("Select start date", value=min_date, min_value=min_date, max_value=max_date)
end_date = date_filter_col2.date_input("Select end date", value=max_date, min_value=min_date, max_value=max_date)

error_placeholder = st.empty()

bot_settings_col1, bot_settings_col2 = st.columns(2)
# balance
balance = bot_settings_col1.number_input("Select a balance", min_value=100, max_value=1000000)

# tick rate
tick_rate = bot_settings_col2.number_input("Select tickrate", min_value=0.3, max_value=1.0, step=0.1, value=0.5)

st.markdown("---")

control_col1, control_col2 = st.columns(2)
button_col1, button_col2 = control_col1.columns(2)

# Bot start button
bot_start = button_col1.button("Start / Restart Trading Bot")
# Bot stop button
bot_stop = button_col2.button("Stop")

# creating a single-element container
plots_placeholder = st.empty()

example_stocks = ['IP', 'DVA', 'ORLY', 'CME', 'BR', 'UHS', 'TAP', 'NEM', 'SHW', 'FAST', 'HAL', 'LRCX', 'MO', 'DGX', 'KO', 'FE', 'META', 'IVZ', 'XEL', 'MTB', 'PPL', 'MRK', 'CCI', 'TEL', 'F', 'T', 'WRB', 'NDSN', 'JKHY', 'DRI', 'ZBRA', 'PGR', 'DOV', 'BMY', 'GLW', 'MRO', 'K', 'ISRG', 'LNT', 'EBAY', 'KLAC', 'GNRC', 'CARR', 'PNW', 'LMT', 'AON', 'MRNA', 'NWSA', 'APTV', 'IT', 'IRM', 'MCO', 'RTX', 'INCY', 'BLK', 'DAL', 'BDX', 'AWK', 'COST', 'CBRE', 'TGT', 'TSN', 'DFS', 'ADSK', 'CTRA', 'INTC', 'HAS', 'TSLA', 'BIO', 'CMI', 'TXN', 'CRM', 'STT', 'WTW', 'ALL', 'CHTR', 'CPRT', 'QRVO', 'AIZ', 'MTD', 'CPT', 'CHD', 'TDG', 'TSCO', 'MHK', 'RL', 'EMR', 'ACGL', 'RHI', 'RSG', 'KEYS', 'GEN', 'TMO', 'A', 'EMN', 'CTAS', 'HES', 'MA', 'WRK', 'EL', 'UPS', 'IQV', 'IBM', 'LHX', 'BEN', 'MTCH', 'CSCO', 'GPC', 'PSA', 'ECL', 'ETN', 'ICE', 'CVS', 'AJG', 'HUM', 'SRE', 'L', 'VRSN', 'GIS', 'HON', 'BBWI', 'BALL', 'BRK.B', 'POOL', 'SPGI', 'ETR', 'FANG', 'BBY', 'WEC', 'TFC', 'AMD', 'BKNG', 'CF', 'GRMN', 'WYNN', 'WFC', 'TFX', 'WMT', 'AEE', 'CTVA', 'ALLE', 'ILMN', 'SYK', 'ALK', 'CPB', 'DOW', 'IEX', 'BRO', 'DD', 'BAC', 'NI', 'ZTS', 'AME', 'AVB', 'VTR', 'CL', 'SEE', 'IR', 'NDAQ', 'GPN', 'DHI', 'ROL', 'PCAR', 'DPZ', 'STX', 'URI', 'HOLX', 'CBOE', 'WAB', 'KHC', 'GM', 'FMC', 'SNPS', 'FTNT', 'AMGN', 'EXPD', 'NKE', 'MDLZ', 'BK', 'PTC', 'DE', 'NCLH', 'ROP', 'TMUS', 'CNP', 'MMM', 'LYB', 'BXP', 'MGM', 'CTSH', 'VTRS', 'EVRG', 'GE', 'USB', 'XRAY', 'PXD', 'RF', 'CE', 'MDT', 'RCL', 'PFE', 'MOS', 'EW', 'TECH', 'AVGO', 'KIM', 'MSFT', 'LW', 'C', 'CAG', 'EIX', 'ADI', 'TROW', 'MCHP', 'ODFL', 'TRV', 'ADBE', 'WBD', 'SWKS', 'DIS', 'DXCM', 'MCD', 'PYPL', 'LIN', 'ROST', 'BF.B', 'SNA', 'MNST', 'CDNS', 'PEP', 'EQIX', 'STLD', 'EQR', 'GL', 'AES', 'VZ', 'WAT', 'GOOGL', 'OMC', 'CMA', 'PPG', 'SBUX', 'EXC', 'GS', 'HPQ', 'AMZN', 'COP', 'ABBV', 'EOG', 'HRL', 'TJX', 'VRTX', 'ELV', 'FFIV', 'BKR', 'PARA', 'PNR', 'FTV', 'VFC', 'PKG', 'TPR', 'AIG', 'TDY', 'APH', 'NTAP', 'HST', 'EFX', 'HD', 'V', 'AEP', 'AAL', 'WY', 'ES', 'PEG', 'SLB', 'PFG', 'NSC', 'CAH', 'AKAM', 'FSLR', 'MAA', 'IPG', 'HSY', 'PM', 'ROK', 'ZION', 'NXPI', 'GILD', 'ESS', 'HBAN', 'CRL', 'LH', 'XOM', 'HLT', 'LVS', 'DUK', 'MAR', 'SPG', 'OKE', 'ORCL', 'VLO', 'FOXA', 'KMX', 'ARE', 'LEN', 'WST', 'FDX', 'UNH', 'WM', 'HWM', 'ENPH', 'HIG', 'STZ', 'KMB', 'PG', 'NWS', 'OTIS', 'MCK', 'WMB', 'TER', 'GD', 'CFG', 'IFF', 'PAYX', 'STE', 'NFLX', 'SBAC', 'WBA', 'J', 'BSX', 'LDOS', 'KDP', 'SO', 'UNP', 'MKTX', 'ANSS', 'SEDG', 'AMAT', 'KMI', 'NTRS', 'CAT', 'PEAK', 'JPM', 'PHM', 'FITB', 'MMC', 'MU', 'FLT', 'CHRW', 'LYV', 'TYL', 'NVDA', 'COO', 'MPWR', 'AAPL', 'MSI', 'SJM', 'PNC', 'CSGP', 'NEE', 'WHR', 'PCG', 'ED', 'AZO', 'HCA', 'EPAM', 'CVX', 'O', 'LUV', 'FOX', 'SYY', 'REGN', 'BIIB', 'ALGN', 'CDW', 'CDAY', 'ABT', 'JCI', 'BA', 'FCX', 'FDS', 'TTWO', 'PAYC', 'APD', 'BAX', 'OXY', 'QCOM', 'PSX', 'INTU', 'PH', 'CSX', 'EQT', 'ATO', 'ON', 'ITW', 'REG', 'NOW', 'TT', 'MLM', 'MPC', 'NOC', 'LLY', 'CMG', 'EXPE', 'INVH', 'FRT', 'GOOG', 'ALB', 'DTE', 'CMS', 'TRMB', 'SWK', 'COF', 'ULTA', 'EXR', 'LKQ', 'FIS', 'VMC', 'CTLT', 'ETSY', 'TRGP', 'NUE', 'VRSK', 'D', 'XYL', 'RMD', 'ADM', 'MSCI', 'HII', 'UAL', 'VICI', 'HSIC', 'CINF', 'AMP', 'PWR', 'MAS', 'SYF', 'ANET', 'AOS', 'KEY', 'GWW', 'AMT', 'CCL', 'PRU', 'UDR', 'NRG', 'LOW', 'JNJ', 'AFL', 'BWA', 'SCHW', 'DLR', 'IDXX', 'DHR', 'CLX', 'TXT', 'MET', 'NVR', 'APA', 'MS', 'ADP', 'HPE', 'JNPR', 'CMCSA', 'CI', 'DG', 'DLTR', 'CNC', 'JBHT', 'ACN', 'AVY', 'PLD', 'EA', 'DVN', 'RJF', 'WELL', 'CEG', 'YUM', 'KR', 'AXP', 'ZBH', 'MOH', 'MKC', 'CB', 'WDC', 'CZR', 'AMCR']

if bot_start and (start_date < end_date):
    sp500_filtered_df = filter_sp500_dataset(sp500_df, start_date, end_date)
    balance_list = []
    ticks = 0
    stock_portfolio = {}

    # near real-time / live feed simulation
    while ticks < len(sp500_filtered_df):
        
        if bot_stop:
            break

        sp500_stream_df = sp500_filtered_df.iloc[:ticks]

        # UPDATE BALANCE HERE
        balance_list.append(random.randint(10,15))

        current_date = sp500_filtered_df.iloc[ticks]['Date']

        # UPDATE PORTFOLIO BASED ON BOT
        for i in random.sample(example_stocks, 1):
            stock_portfolio[i] = random.randint(1,10)

        with plots_placeholder.container():

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
                                            yaxis_title="Price")
                
                # Disable draggable date filter
                candlestick_fig.update_xaxes(
                    rangeslider_visible=False,
                    rangebreaks=[
                        # NOTE: Below values are bound (not single values), ie. hide x to y
                        dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
                    ]
                )

                st.plotly_chart(candlestick_fig)

                portfolio_fig = go.Figure(data=[go.Pie(labels=list(stock_portfolio.keys()), values=list(stock_portfolio.values()))])
                portfolio_fig.update_layout(
                    title="Stock Portfolio Distribution",
                    title_x=0.5  # Center the title
                )
                st.plotly_chart(portfolio_fig)

            with fig_col2:
                balance_fig = px.line(
                    balance_list,
                    title="Balance of Trading bot",
                    
                )
                balance_fig.update_layout(xaxis_title="Balance", showlegend=False)
                st.plotly_chart(balance_fig)

            ticks += 1
            time.sleep(tick_rate)

elif end_date < start_date:
    error_placeholder.error("End date cannot be before start date.")

st.markdown("---")