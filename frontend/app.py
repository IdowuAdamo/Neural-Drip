import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Adds C:/Code/neural_drip to path

import streamlit as st
from backend.models.recommendation import get_recommendations

st.title("Neural-Drip: Price Comparison System")
query = st.text_input("Enter product (e.g., 'affordable phone')")
budget = st.number_input("Enter your budget (₦)", min_value=0)
num_results = st.slider("Number of results", 1, 10, 3)

if st.button("Search"):
    st.write("### Recommendations")
    recommendation = get_recommendations(query, budget, num_results)
    st.markdown(recommendation) 