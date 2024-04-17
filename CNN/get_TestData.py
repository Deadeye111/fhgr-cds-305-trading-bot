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
    symbols = ['AAPL', 'MSFT', 'GOOGL']    
    download_stock_data(symbols)

