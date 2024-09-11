import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
import os

# Load all processed stock data and sentiment data from specified directories
def load_data(stock_dir, sentiment_dir):
    all_data = []

    # Load and merge all stock data files
    for filename in os.listdir(stock_dir):
        if filename.endswith("_stock_data.csv"):
            stock_file = os.path.join(stock_dir, filename)
            print(f"Loading stock data from: {stock_file}")
            stock_data = pd.read_csv(stock_file)

            if 'Date' in stock_data.columns:
                stock_data.rename(columns={'Date': 'date'}, inplace=True)

            if 'date' not in stock_data.columns:
                print(f"Error: 'date' column not found in stock data from {filename}.")
                continue

            stock_data['date'] = pd.to_datetime(stock_data['date'])
            stock_data['date'] = stock_data['date'].dt.tz_localize(None)

            all_data.append(stock_data)

    # Concatenate all stock data into a single DataFrame
    stock_data_combined = pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()
    print(f"Combined Stock Data Shape: {stock_data_combined.shape}")

    all_data = []

    # Load and merge all sentiment data files
    for filename in os.listdir(sentiment_dir):
        if filename.endswith("_news.csv"):
            sentiment_file = os.path.join(sentiment_dir, filename)
            print(f"Loading sentiment data from: {sentiment_file}")
            sentiment_data = pd.read_csv(sentiment_file)

            if 'publishedAt' in sentiment_data.columns:
                sentiment_data.rename(columns={'publishedAt': 'date'}, inplace=True)

            if 'date' not in sentiment_data.columns:
                print(f"Error: 'date' column not found in sentiment data from {filename}.")
                continue

            sentiment_data['date'] = pd.to_datetime(sentiment_data['date'], errors='coerce', utc=True)
            sentiment_data['date'] = sentiment_data['date'].dt.tz_localize(None)
            sentiment_data = sentiment_data.dropna(subset=['date'])
            sentiment_data = sentiment_data[sentiment_data['date'] > pd.Timestamp('1970-01-01')]

            all_data.append(sentiment_data)

    # Concatenate all sentiment data into a single DataFrame
    sentiment_data_combined = pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()
    print(f"Combined Sentiment Data Shape: {sentiment_data_combined.shape}")

    # Print date ranges for both datasets
    if not stock_data_combined.empty:
        print(f"Stock data date range: {stock_data_combined['date'].min()} to {stock_data_combined['date'].max()}")
    if not sentiment_data_combined.empty:
        print(f"Sentiment data date range: {sentiment_data_combined['date'].min()} to {sentiment_data_combined['date'].max()}")

    # Merge all stock and sentiment data on 'date'
    if stock_data_combined.empty or sentiment_data_combined.empty:
        print("Error: One or both of the datasets are empty.")
        return None

    merged_data = pd.merge(stock_data_combined, sentiment_data_combined, on="date", how="inner")
    print(f"Data merged successfully. Total rows: {len(merged_data)}")

    # Print a sample of the merged data for debugging
    print(merged_data.head())

    if 'sentiment' not in merged_data.columns:
        print("Error: 'sentiment' column not found in merged data.")
        return None
    if 'Close' not in merged_data.columns:
        print("Error: 'Close' column not found in merged data.")
        return None

    return merged_data

# Train a basic linear regression model
def train_model(data):
    if data is None or data.empty:
        print("Error: No data available to train the model.")
        return None

    # Ensure there are no NaN values in features or target
    data = data.dropna(subset=['sentiment', 'Close'])

    if data.empty:
        print("Error: Data is empty after dropping NaNs.")
        return None

    X = data[['sentiment']]  # Features (only sentiment in this case)
    y = data['Close']  # Target (stock price)

    # Splitting the dataset into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Linear regression model training
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Model evaluation
    y_pred = model.predict(X_test)
    r2_score = model.score(X_test, y_test)
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)

    print(f"Model trained with R^2 score: {r2_score}")
    print(f"Mean Squared Error: {mse}")
    print(f"Mean Absolute Error: {mae}")

    return model

if __name__ == "__main__":
    # Load the stock and sentiment data
    data = load_data("data/processed", "data/processed_with_sentiment")
    
    # Train and evaluate the model
    model = train_model(data)
