# app.py
# This script provides a Streamlit web interface for predicting Bengaluru home prices.

import streamlit as st
import util

st.title("Bengaluru Home Price Prediction")
st.sidebar.header("Input Features")

# Load artifacts
util.load_saved_artifacts()

# Inputs
locations = util.get_location_names()
location = st.sidebar.selectbox("Location", locations)
sqft = st.sidebar.number_input("Total Square Feet", min_value=300, max_value=10000, step=50)
bhk = st.sidebar.number_input("Number of Bedrooms (BHK)", min_value=1, max_value=10, step=1)
bath = st.sidebar.number_input("Number of Bathrooms", min_value=1, max_value=10, step=1)

if st.sidebar.button("Estimate Price"):
    price = util.get_estimated_price(location, sqft, bath, bhk)
    st.success(f"Estimated Price: {price} lakhs")
