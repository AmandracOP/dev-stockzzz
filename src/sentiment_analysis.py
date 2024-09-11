from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import os

# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Function to calculate sentiment score
def calculate_sentiment(text):
    return analyzer.polarity_scores(text)['compound']

# Apply sentiment analysis to news data
def analyze_sentiment(file_path):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} does not exist.")
        return
    
    df = pd.read_csv(file_path)
    
    if 'cleaned_text' not in df.columns:
        print("Error: 'cleaned_text' column not found in the news data.")
        return df
    
    # Calculate sentiment only for non-empty texts
    df['sentiment'] = df['cleaned_text'].apply(lambda text: calculate_sentiment(text) if pd.notnull(text) else 0)
    
    # Create directory for saving processed file if it doesn't exist
    processed_file_path = file_path.replace('processed', 'processed_with_sentiment')
    os.makedirs(os.path.dirname(processed_file_path), exist_ok=True)
    
    df.to_csv(processed_file_path, index=False)
    print(f"Sentiment analysis complete. File saved to {processed_file_path}")
    return df

if __name__ == "__main__":
    # List of news files for different companies
    company_files = [
        "data/processed/Apple_news.csv",
        "data/processed/Amazon_news.csv",
        "data/processed/Google_news.csv",
        "data/processed/Microsoft_news.csv",
        "data/processed/Tesla_news.csv"
    ]
    
    for file_path in company_files:
        analyze_sentiment(file_path)
