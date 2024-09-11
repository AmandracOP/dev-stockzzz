import pandas as pd
import os
import spacy

# Initialize spaCy model
nlp = spacy.load("en_core_web_sm")

# Function to clean stock data (e.g., removing NaNs)
def clean_stock_data(file_path):
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: {file_path} does not exist.")
        return
    
    df = pd.read_csv(file_path)
    df.dropna(inplace=True)  # Removing rows with missing values
    
    # Construct processed file path
    processed_file_path = file_path.replace('raw', 'processed')
    os.makedirs(os.path.dirname(processed_file_path), exist_ok=True)  # Ensure directory exists
    
    df.to_csv(processed_file_path, index=False)
    print(f"Processed stock data saved to {processed_file_path}")
    return df

# Function to preprocess news data
def preprocess_news(file_path):
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: {file_path} does not exist.")
        return
    
    df = pd.read_csv(file_path)
    
    # Check if 'description' column exists
    if 'description' not in df.columns:
        print("Error: 'description' column not found in the news data.")
        return df
    
    # Basic NLP preprocessing (tokenization, lemmatization)
    def process_text(text):
        doc = nlp(text)
        tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
        return " ".join(tokens)
    
    # Apply processing to the 'description' column
    df['cleaned_text'] = df['description'].apply(lambda x: process_text(x) if pd.notnull(x) else "")
    
    # Construct processed file path
    processed_file_path = file_path.replace('raw', 'processed')
    os.makedirs(os.path.dirname(processed_file_path), exist_ok=True)  # Ensure directory exists
    
    df.to_csv(processed_file_path, index=False)
    print(f"Processed news data saved to {processed_file_path}")
    return df

def process_all_data(companies):
    for company, ticker in companies.items():
        # Process stock data
        stock_data_path = f"data/raw/{ticker}_stock_data.csv"
        print(f"Processing stock data for {company}...")
        clean_stock_data(stock_data_path)
        
        # Process news data
        news_data_path = f"data/raw/{company}_news.csv"
        print(f"Processing news data for {company}...")
        preprocess_news(news_data_path)

if __name__ == "__main__":
    # List of companies and their stock tickers
    companies = {
        'Apple': 'AAPL',
        'Tesla': 'TSLA',
        'Microsoft': 'MSFT',
        'Amazon': 'AMZN',
        'Google': 'GOOGL'
    }
    
    # Process data for all companies
    process_all_data(companies)
