import yfinance as yf
import requests
import os
import pandas as pd
from datetime import datetime

# Function to download stock data using Yahoo Finance
def download_stock_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    file_path = f"data/raw/{ticker}_stock_data.csv"
    data.to_csv(file_path)
    print(f"Stock data for {ticker} saved to {file_path}")
    return data

# Function to fetch news articles using NewsAPI
def fetch_news(query, from_date, to_date, api_key):
    url = f'https://newsapi.org/v2/everything?q={query}&from={from_date}&to={to_date}&pageSize=100&page=1&apiKey={api_key}'
    response = requests.get(url)
    data = response.json()

    # Check if 'articles' exists in the response, and handle errors
    if response.status_code != 200:
        print(f"Error fetching news: {data.get('message', 'Unknown error')}")
        return []

    if 'articles' not in data:
        print(f"Unexpected response format: {data}")
        return []
    
    return data['articles']

# Save news articles to CSV
def save_news(query, from_date, to_date, api_key):
    articles = fetch_news(query, from_date, to_date, api_key)
    
    if articles:
        df = pd.DataFrame(articles)
        file_path = f'data/raw/{query}_news.csv'
        if not os.path.exists('data/raw'):
            os.makedirs('data/raw')
        df.to_csv(file_path, index=False)
        print(f"News data for {query} saved to {file_path}")
    else:
        print(f"No news data collected for {query}")

# Main function to handle multiple companies
def collect_data_for_companies(companies, start_date, end_date, api_key):
    for company, ticker in companies.items():
        print(f"Collecting data for {company} ({ticker})...")
        
        # Download stock data
        download_stock_data(ticker, start_date, end_date)
        
        # Collect news data
        save_news(company, start_date, end_date, api_key)

# Example usage
if __name__ == "__main__":
    # List of companies and their stock tickers
    companies = {
        'Apple': 'AAPL',
        'Tesla': 'TSLA',
        'Microsoft': 'MSFT',
        'Amazon': 'AMZN',
        'Google': 'GOOGL'
    }

    # Time period for data collection
    start_date = '2024-08-11'
    end_date = datetime.today().strftime('%Y-%m-%d')  # Current date in 'YYYY-MM-DD' format

    # News API key
    api_key = '1e1cdf0caebf4ace8eda398bb10ea357'

    # Collect data for all companies
    collect_data_for_companies(companies, start_date, end_date, api_key)
