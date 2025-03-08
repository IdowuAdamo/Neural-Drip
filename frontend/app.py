import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add project root to path

import streamlit as st
from backend.models.recommendation import get_recommendations

# page title and layout
st.title("Neural-Drip: Price Comparison System")
st.write("Find the best deals on products within your budget!")

# user input fields
query = st.text_input("Enter product (e.g., 'affordable phone')", value="affordable phone under ₦80,000")
budget = st.number_input("Enter your budget (₦)", min_value=0, value=80000, step=1000)
num_results = st.slider("Number of results", min_value=1, max_value=10, value=3)

# Search button and results display
if st.button("Search"):
    st.write("### Recommendations")
    with st.spinner("Fetching recommendations..."):
        recommendation = get_recommendations(query, budget, num_results)
        st.markdown(recommendation, unsafe_allow_html=True)  # Render HTML for clickable links