import yfinance as yf
import os

if __name__ == '__main__':
    print('Downloading S&P 500 data...')
    data = yf.download('^GSPC', start= '2023-01-01', end='2024-03-31')
    file_path = os.path.join('data_SP500', f'sp500.csv')
    data.to_csv(file_path)
    print('Data downloaded and saved to', file_path)