import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add project root to path

import streamlit as st
from backend.models.recommendation import get_recommendations

# Page title and layout
st.title("BestBuy: Product Recommendation System")
st.write("Find the best deals on quality products within your budget!")

# User input fields
query = st.text_input("Enter product (e.g., 'affordable phone')", value="affordable phone fit for content creation")
budget = st.number_input("Enter your budget (₦)", min_value=0, value=95000, step=1000)
num_results = st.slider("Number of results", min_value=1, max_value=5, value=2)
source_filter = st.selectbox("Filter by source", ["All", "Jumia", "Konga"], index=0)

# Search button and results display
if st.button("Search"):
    st.write("### Recommendations")
    with st.spinner("Fetching recommendations..."):
        # Pass source_filter to get_recommendations
        recommendation = get_recommendations(query, budget, num_results, source_filter)
        st.markdown(recommendation, unsafe_allow_html=True)  # Render HTML for clickable links