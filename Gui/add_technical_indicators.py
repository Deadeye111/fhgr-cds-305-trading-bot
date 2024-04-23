import numpy as np
import pandas as pd

from ta.trend import TRIXIndicator
from ta.trend import WMAIndicator
from ta.trend import CCIIndicator
from ta.volume import money_flow_index
import pandas_ta as pta
from ta.trend import MACD
from ta.momentum import PercentagePriceOscillator
from ta.momentum import ROCIndicator
from ta.volume import ChaikinMoneyFlowIndicator
from ta.trend import ADXIndicator
from ta.volatility import AverageTrueRange
from ta.volatility import BollingerBands


#Simple Moving Average - SMA
def get_SMA(df, window):
    for i in window:
        df[f"SMA_{i}"] = df['Close'].rolling(window=i).mean()
    return df

#Exponential Moving Average - EMA
def get_EMA(df, window):
    for i in window:
        df[f"EMA_{i}"] = df['Close'].ewm(span=i, adjust=False).mean()
    return df

#Triple Exponential Moving Average
def get_TRIX(df, window):
    for i in window:
        trix_values = TRIXIndicator(df['Close'], i).trix()
        df[f"TRIX_{i}"] = trix_values
    return df

#Money FLow Index - MFI
def get_MFI(df, window):
    for i in window:
        df[f"money_flow_index_{i}"] = money_flow_index(df['High'], df['Low'], df['Close'], df['Volume'], window=i)
    return df  

#Relative Strength Index - RSI
def get_RSI_smooth(df, window):

    prev_rsi = np.inf
    prev_avg_gain = np.inf
    prev_avg_loss = np.inf
    rolling_count = 0

    def calculate_RSI(series, period):
        # nonlocal rolling_count
        nonlocal prev_avg_gain
        nonlocal prev_avg_loss
        nonlocal rolling_count

        curr_gains = series.where(series >= 0, 0)  # replace 0 where series not > 0
        curr_losses = np.abs(series.where(series < 0, 0))
        avg_gain = curr_gains.sum() / period  # * 100
        avg_loss = curr_losses.sum() / period  # * 100
        rsi = -1

        if rolling_count == 0:
            # first RSI calculation
            rsi = 100 - (100 / (1 + (avg_gain / avg_loss)))
            # print(rolling_count,"rs1=",rs, rsi)
        else:
            # smoothed RSI
            # current gain and loss should be used, not avg_gain & avg_loss
            rsi = 100 - (100 / (1 + ((prev_avg_gain * (period - 1) + curr_gains.iloc[-1]) /
                                     (prev_avg_loss * (period - 1) + curr_losses.iloc[-1]))))
            # print(rolling_count,"rs2=",rs, rsi)

        # df['rsi_'+str(period)+'_own'][period + rolling_count] = rsi
        rolling_count = rolling_count + 1
        prev_avg_gain = avg_gain
        prev_avg_loss = avg_loss
        return rsi

    diff = df['Close'].diff()[1:]  # skip na
    for i in window:
        df['rsi_' + str(i)] = np.nan
        # df['rsi_'+str(period)+'_own_1'] = np.nan
        rolling_count = 0
        res = diff.rolling(i).apply(calculate_RSI, args=(i,), raw=False)
        df['rsi_' + str(i)][1:] = res
    return df

#Williams %R
def get_WILLIAMS_R(df, window):
    for i in window:
        highest_high = df['High'].rolling(window=i).max()
        lowest_low = df['Low'].rolling(window=i).min()
        df[f"williams_r_{i}"] = ((highest_high - df['Close']) / (highest_high - lowest_low)) * (-100)
    return df

#Weighted Mobing Average - WMA
def get_WMA(df, window):
    for i in window:
        df[f"wma_{i}"] = WMAIndicator(df['Close'], i).wma()
    return df

#Hull Moving Average - HMA
def get_HMA(df, window):
    for i in window:
        wma1 = 2 * df['Close'].rolling(window=int(i / 2)).mean()
        wma2 = df['Close'].rolling(window=i).mean()
        diff = wma1 - wma2
        hma = diff.rolling(window=int(np.sqrt(i))).mean()
        df[f"hma_{i}"] = hma
    return df

#Commondity Channel Index - CCI
def get_CCI(df, window):
    for i in window:
        cci_values = CCIIndicator(df['High'], df['Low'], df['Close'], i).cci()
        df[f"cci_{i}"] = cci_values
    return df

#Chande Momentum Oscillator - CMO
def get_CMO(df, window):
    for i in window:
        df[f"cmo_{i}"] = pta.cmo(df['Close'], length=i)
    return df

#Moving Average Convergence Divergence - MACD
def get_MACD(df):
    macd_object = MACD(df['Close'])
    df['MACD'] = macd_object.macd()
    df['MACD_Signal'] = macd_object.macd_signal()
    df['MACD_Diff'] = macd_object.macd_diff()
    return df

#Percentage Price Oscillator - PPO
def get_PPO(df):
    ppo_object = PercentagePriceOscillator(df['Close'])
    df[f"PPO"] = ppo_object.ppo()
    df[f"PPO_Histogram"] = ppo_object.ppo_hist()
    df[f"PPO_Signal"] = ppo_object.ppo_signal()
    return df

#Rate of Change - ROC
def get_ROC(df, window):
    for i in window:
        df[f"ROC_{i}"] = ROCIndicator(df['Close'], i).roc()
    return df

#Chaikin Money Flow - CMF
def get_CMF(df, window):
    for i in window:
        df[f"cmf_{i}"] = ChaikinMoneyFlowIndicator(df['High'], df['Low'], df['Close'], df['Volume'], i).chaikin_money_flow()
    return df

#Average Directional Movement Index - ADX
def get_ADX(df, window):
    for i in window:
        df[f"adx_{i}"] = ADXIndicator(df['High'], df['Low'], df['Close'], i).adx()
        df[f"adx_pos_{i}"] = ADXIndicator(df['High'], df['Low'], df['Close'], i).adx_pos()
        df[f"adx_neg_{i}"] = ADXIndicator(df['High'], df['Low'], df['Close'], i).adx_neg()
    return df

#Average True Range - ATR
def get_ATR(df, window):
    for i in window:
        df[f"atr_{i}"] = AverageTrueRange(df['High'], df['Low'], df['Close'], i).average_true_range()
    return df

#Bollinger Bands
def get_BollingerBands(df, window):
    for i in window:
        bb = BollingerBands(df['Close'], window=i, window_dev=2)
        df[f"bb_bbm_{i}"] = bb.bollinger_mavg()
        df[f"bb_bbh_{i}"] = bb.bollinger_hband()
        df[f"bb_bbl_{i}"] = bb.bollinger_lband()
    return df


def add_technical_indicators(data, func_windows=[3,5,7,9,11,13,15,17,19,21]):
    #calculate all the indicators
    data = get_SMA(data, func_windows)
    data = get_EMA(data, func_windows)
    data = get_TRIX(data, func_windows)
    data = get_MFI(data, func_windows)
    data = get_RSI_smooth(data, func_windows)
    data = get_WILLIAMS_R(data, func_windows)
    data = get_WMA(data, func_windows)
    data = get_HMA(data, func_windows)
    data = get_CCI(data, func_windows)
    data = get_CMO(data, func_windows)
    data = get_MACD(data)
    data = get_PPO(data)
    data = get_ROC(data, func_windows)
    data = get_CMF(data, func_windows)
    data = get_ADX(data, func_windows)
    data = get_ATR(data, func_windows)
    data = get_BollingerBands(data, func_windows)
    return data
