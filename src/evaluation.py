import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from model import load_data, train_model

# Function to evaluate model performance
def evaluate_model(model, data):
    if model is None or data is None or data.empty:
        print("Error: Invalid model or data.")
        return

    X = data[['sentiment']]
    y = data['Close']
    
    # Predict stock prices
    predictions = model.predict(X)
    
    # Calculate Mean Squared Error
    mse = mean_squared_error(y, predictions)
    print(f"Mean Squared Error: {mse}")
    
    # Ensure dates are sorted for plotting
    data_sorted = data.sort_values(by='date')
    
    # Plotting actual vs predicted stock prices
    plt.figure(figsize=(10, 6))
    plt.plot(data_sorted['date'], data_sorted['Close'], label='Actual Prices')
    plt.plot(data_sorted['date'], predictions, label='Predicted Prices', linestyle='dashed')
    plt.xlabel('Date')
    plt.ylabel('Stock Price')
    plt.title('Stock Price Prediction vs Actual')
    plt.legend()
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Load the stock and sentiment data from directories
    data = load_data("data/processed", "data/processed_with_sentiment")
    
    # Train the model
    model = train_model(data)
    
    # Evaluate the model
    evaluate_model(model, data)
