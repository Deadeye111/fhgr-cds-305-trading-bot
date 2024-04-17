import os
import yfinance as yf



def download_stock_data(symbols):
    """
    Herunterladen von Aktiendaten mit yfinance und Speichern in CSV-Dateien.

    Parameter:
    - symbols: Eine Liste von Aktiensymbolen (z.B. ['AAPL', 'MSFT', 'GOOGL'])

    Rückgabewert:
    - None
    """
    for symbol in symbols:
        data = yf.download(symbol, start= '2023-01-01', end='2024-03-31')
        file_path = os.path.join('test_data/', f'{symbol}.csv')
        data.to_csv(file_path)
        
        print(f'Aktiendaten für {symbol} heruntergeladen und in {file_path} gespeichert.')



if __name__ == "__main__":
    # Symbols of companies in S&P500 in Test Data    
    symbols = ['IP', 'DVA', 'ORLY', 'CME', 'BR', 'UHS', 'TAP', 'NEM', 'SHW', 'FAST', 'HAL', 'LRCX', 'MO', 'DGX', 'KO', 'FE', 'META', 'IVZ', 'XEL', 'MTB', 'PPL', 'MRK', 'CCI', 'TEL', 'F', 'T', 'WRB', 'NDSN', 'JKHY', 'DRI', 'ZBRA', 'PGR', 'DOV', 'BMY', 'GLW', 'MRO', 'K', 'ISRG', 'LNT', 'EBAY', 'KLAC', 'GNRC', 'CARR', 'PNW', 'LMT', 'AON', 'MRNA', 'NWSA', 'APTV', 'IT', 'IRM', 'MCO', 'RTX', 'INCY', 'BLK', 'DAL', 'BDX', 'AWK', 'COST', 'CBRE', 'TGT', 'TSN', 'DFS', 'ADSK', 'CTRA', 'INTC', 'HAS', 'TSLA', 'BIO', 'CMI', 'TXN', 'CRM', 'STT', 'WTW', 'ALL', 'CHTR', 'CPRT', 'QRVO', 'AIZ', 'MTD', 'CPT', 'CHD', 'TDG', 'TSCO', 'MHK', 'RL', 'EMR', 'ACGL', 'RHI', 'RSG', 'KEYS', 'GEN', 'TMO', 'A', 'EMN', 'CTAS', 'HES', 'MA', 'WRK', 'EL', 'UPS', 'IQV', 'IBM', 'LHX', 'BEN', 'MTCH', 'CSCO', 'GPC', 'PSA', 'ECL', 'ETN', 'ICE', 'CVS', 'AJG', 'HUM', 'SRE', 'L', 'VRSN', 'GIS', 'HON', 'BBWI', 'BALL', 'BRK.B', 'POOL', 'SPGI', 'ETR', 'FANG', 'BBY', 'WEC', 'TFC', 'AMD', 'BKNG', 'CF', 'GRMN', 'WYNN', 'WFC', 'TFX', 'WMT', 'AEE', 'CTVA', 'ALLE', 'ILMN', 'SYK', 'ALK', 'CPB', 'DOW', 'IEX', 'BRO', 'DD', 'BAC', 'NI', 'ZTS', 'AME', 'AVB', 'VTR', 'CL', 'SEE', 'IR', 'NDAQ', 'GPN', 'DHI', 'ROL', 'PCAR', 'DPZ', 'STX', 'URI', 'HOLX', 'CBOE', 'WAB', 'KHC', 'GM', 'FMC', 'SNPS', 'FTNT', 'AMGN', 'EXPD', 'NKE', 'MDLZ', 'BK', 'PTC', 'DE', 'NCLH', 'ROP', 'TMUS', 'CNP', 'MMM', 'LYB', 'BXP', 'MGM', 'CTSH', 'VTRS', 'EVRG', 'GE', 'USB', 'XRAY', 'PXD', 'RF', 'CE', 'MDT', 'RCL', 'PFE', 'MOS', 'EW', 'TECH', 'AVGO', 'KIM', 'MSFT', 'LW', 'C', 'CAG', 'EIX', 'ADI', 'TROW', 'MCHP', 'ODFL', 'TRV', 'ADBE', 'WBD', 'SWKS', 'DIS', 'DXCM', 'MCD', 'PYPL', 'LIN', 'ROST', 'BF.B', 'SNA', 'MNST', 'CDNS', 'PEP', 'EQIX', 'STLD', 'EQR', 'GL', 'AES', 'VZ', 'WAT', 'GOOGL', 'OMC', 'CMA', 'PPG', 'SBUX', 'EXC', 'GS', 'HPQ', 'AMZN', 'COP', 'ABBV', 'EOG', 'HRL', 'TJX', 'VRTX', 'ELV', 'FFIV', 'BKR', 'PARA', 'PNR', 'FTV', 'VFC', 'PKG', 'TPR', 'AIG', 'TDY', 'APH', 'NTAP', 'HST', 'EFX', 'HD', 'V', 'AEP', 'AAL', 'WY', 'ES', 'PEG', 'SLB', 'PFG', 'NSC', 'CAH', 'AKAM', 'FSLR', 'MAA', 'IPG', 'HSY', 'PM', 'ROK', 'ZION', 'NXPI', 'GILD', 'ESS', 'HBAN', 'CRL', 'LH', 'XOM', 'HLT', 'LVS', 'DUK', 'MAR', 'SPG', 'OKE', 'ORCL', 'VLO', 'FOXA', 'KMX', 'ARE', 'LEN', 'WST', 'FDX', 'UNH', 'WM', 'HWM', 'ENPH', 'HIG', 'STZ', 'KMB', 'PG', 'NWS', 'OTIS', 'MCK', 'WMB', 'TER', 'GD', 'CFG', 'IFF', 'PAYX', 'STE', 'NFLX', 'SBAC', 'WBA', 'J', 'BSX', 'LDOS', 'KDP', 'SO', 'UNP', 'MKTX', 'ANSS', 'SEDG', 'AMAT', 'KMI', 'NTRS', 'CAT', 'PEAK', 'JPM', 'PHM', 'FITB', 'MMC', 'MU', 'FLT', 'CHRW', 'LYV', 'TYL', 'NVDA', 'COO', 'MPWR', 'AAPL', 'MSI', 'SJM', 'PNC', 'CSGP', 'NEE', 'WHR', 'PCG', 'ED', 'AZO', 'HCA', 'EPAM', 'CVX', 'O', 'LUV', 'FOX', 'SYY', 'REGN', 'BIIB', 'ALGN', 'CDW', 'CDAY', 'ABT', 'JCI', 'BA', 'FCX', 'FDS', 'TTWO', 'PAYC', 'APD', 'BAX', 'OXY', 'QCOM', 'PSX', 'INTU', 'PH', 'CSX', 'EQT', 'ATO', 'ON', 'ITW', 'REG', 'NOW', 'TT', 'MLM', 'MPC', 'NOC', 'LLY', 'CMG', 'EXPE', 'INVH', 'FRT', 'GOOG', 'ALB', 'DTE', 'CMS', 'TRMB', 'SWK', 'COF', 'ULTA', 'EXR', 'LKQ', 'FIS', 'VMC', 'CTLT', 'ETSY', 'TRGP', 'NUE', 'VRSK', 'D', 'XYL', 'RMD', 'ADM', 'MSCI', 'HII', 'UAL', 'VICI', 'HSIC', 'CINF', 'AMP', 'PWR', 'MAS', 'SYF', 'ANET', 'AOS', 'KEY', 'GWW', 'AMT', 'CCL', 'PRU', 'UDR', 'NRG', 'LOW', 'JNJ', 'AFL', 'BWA', 'SCHW', 'DLR', 'IDXX', 'DHR', 'CLX', 'TXT', 'MET', 'NVR', 'APA', 'MS', 'ADP', 'HPE', 'JNPR', 'CMCSA', 'CI', 'DG', 'DLTR', 'CNC', 'JBHT', 'ACN', 'AVY', 'PLD', 'EA', 'DVN', 'RJF', 'WELL', 'CEG', 'YUM', 'KR', 'AXP', 'ZBH', 'MOH', 'MKC', 'CB', 'WDC', 'CZR', 'AMCR']    
    download_stock_data(symbols)

