# train_model.py
# This script trains a regression model to predict Bengaluru home prices.
# It preprocesses the data, trains the model, and saves the model and feature names as artifacts.

import pandas as pd
import numpy as np
import pickle
import json
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

def convert_sqft_to_num(sqft):
    try:
        # Handle ranges like "2100 - 2850"
        tokens = sqft.split('-')
        if len(tokens) == 2:
            return (float(tokens[0]) + float(tokens[1])) / 2
        # Handle cases like "34.46Sq. Meter"
        return float(sqft.split('Sq.')[0].strip())
    except:
        return None

def preprocess_data(data_path):
    df = pd.read_csv(data_path)
    # Drop unnecessary columns
    df = df.drop(['area_type', 'availability', 'society', 'balcony'], axis=1)
    # Convert total_sqft to numeric
    df['total_sqft'] = df['total_sqft'].apply(convert_sqft_to_num)
    # Extract bhk from size
    df['bhk'] = df['size'].apply(lambda x: int(x.split(' ')[0]) if isinstance(x, str) else None)
    # Drop rows with missing or invalid data
    df = df.dropna()
    df = df[df['bath'] < df['bhk'] + 2]  # Remove outliers
    # One-hot encoding for location
    dummies = pd.get_dummies(df['location'], drop_first=True)
    df = pd.concat([df, dummies], axis=1)
    df = df.drop(['location', 'size'], axis=1)
    return df

def train_model(df):
    X = df.drop(['price'], axis=1)
    y = df['price']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    print("Model trained. RMSE:", np.sqrt(mean_squared_error(y_test, model.predict(X_test))))
    return model, X.columns

if __name__ == "__main__":
    data_path = r"D:\download\Bengaluru_House_Data.csv"
    df = preprocess_data(data_path)
    model, feature_columns = train_model(df)
    # Save model
    with open("banglore_home_prices_model.pickle", "wb") as f:
        pickle.dump(model, f)
    # Save feature columns
    with open("columns.json", "w") as f:
        json.dump({"data_columns": feature_columns.tolist()}, f)
    print("Artifacts saved: banglore_home_prices_model.pickle, columns.json")