# Stock Market Prediction with NLP & Sentiment Analysis

This project aims to predict stock market trends using sentiment analysis of financial news and historical stock data. We use NLP techniques to analyze the sentiment of news articles and integrate it with time-series stock price data for prediction.

## Project Structure:
- `data/`: Raw and processed data.
- `models/`: Trained machine learning models.
- `notebooks/`: Jupyter notebooks for exploration and visualization.
- `src/`: Source code for data collection, preprocessing, model building, and evaluation.
- `reports/`: Reports and visualizations.

## Installation
1. Clone the repository:
    ```bash
    git clone <repo_url>
    cd devanshi_ds_project
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Datasets
- Stock price data is collected using Yahoo Finance.
- News data is fetched using News API.

## Running the Project
1. Collect data by running `src/data_collection.py`.
2. Preprocess the data using `src/preprocessing.py`.
3. Perform sentiment analysis with `src/sentiment_analysis.py`.
4. Train models using `src/model.py`.
5. Evaluate results with `src/evaluation.py`.
