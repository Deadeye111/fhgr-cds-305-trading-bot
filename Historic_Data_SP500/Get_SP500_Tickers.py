import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
import pandas as pd


def get_archive_urls_timestamps(site_url, start_date, end_date):
    # Extract the base URL
    base_url = urlparse(site_url).netloc
    
    # Fetch the archive page for the website
    archive_url = f"https://web.archive.org/cdx/search/cdx?url={base_url}&output=json"
    response = requests.get(archive_url)
    
    # Parse the JSON response to get the archive URLs
    if response.status_code == 200:
        data = response.json()
        
        # Remove the header row
        data = data[1:]

        wayback_timestamps = []

        for row in data:
            timestamp = row[1]

            if int(timestamp) > int(start_date) and int(timestamp) < int(end_date):
                wayback_timestamps.append(timestamp)
        
        if wayback_timestamps:
            return wayback_timestamps
        else:
            print("No Wayback timestamps in specified period")
            return []

    else:
        print("Failed to fetch archive URLs")
        return []


def getHTMLdocument(url): 
    response = requests.get(url)  # request for HTML document of given url
    return response.text 


def get_sp500_companies_table(timestamp):
    # Scrape tickers contained in S&P500 at given timestamp
    html_document = getHTMLdocument(f'https://web.archive.org/web/{timestamp}/https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    tickers = pd.read_html(html_document)[0]

    return tickers


if __name__ == "__main__":
    start_date = '20150101000000'  # Timestamp Format: yyyymmddhhmmss
    end_date = '20221231000000'    # Timestamp Format: yyyymmddhhmmss
    site_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    timestamps = get_archive_urls_timestamps(site_url, start_date, end_date)
    
    print(f"\nScraped {len(timestamps)} timestamps from web archive..")
    print(f"First Timestamp: {timestamps[0]} | Last Timestamp: {timestamps[-1]}")

    tickers = get_sp500_companies_table(timestamps[0])
