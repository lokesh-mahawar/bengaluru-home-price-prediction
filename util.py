# util.py
# This script provides utility functions to load the model and predict home prices.

import pickle
import json
import numpy as np

__model = None
__data_columns = None

def load_saved_artifacts():
    global __model, __data_columns
    with open("banglore_home_prices_model.pickle", "rb") as f:
        __model = pickle.load(f)
    with open("columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']

def get_location_names():
    return __data_columns[3:]  # Assuming first 3 columns are sqft, bath, bhk

def get_estimated_price(location, sqft, bath, bhk):
    if __model is None or __data_columns is None:
        load_saved_artifacts()
    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if location in __data_columns:
        x[__data_columns.index(location)] = 1
    return round(__model.predict([x])[0], 2)
