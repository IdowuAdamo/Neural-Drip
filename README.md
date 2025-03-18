# AI-Powered Price Comparison & Product Recommendation System

**Overview**
Welcome to the AI-Powered Price Comparison & Product Recommendation System! This project aims to help Nigerians shop smarter by comparing product prices across platforms like Jumia, Konga, Jiji, and Slot in real-time. Our AI analyzes price, durability, and user reviews to recommend the best value-for-money options, empowering users to save money without compromising quality.

**Problem Statement**
With nearly 50% of Nigerians living below the average income (World Bank), finding affordable, durable products is a challenge. This system addresses:
1. Wide price variations across platforms.
2. Time-consuming manual searches.
3. Low-quality, wasteful purchases.

**Core Features**
 1. Real-Time Price Comparison: Scrapes prices from multiple Nigerian e-commerce platforms.
 2. Best Value Recommendations: AI ranks products by price, durability, and reviews.
 3. Budget-Based Search: Filters products within user-defined budgets.
 4. Alternative Suggestions: Offers cheaper or higher-quality options.
 5. Customizable Results: Users choose how many top products to view (e.g., Top 5) with direct purchase links.

 **Project Structure**
Neural-Drip/
├── data/
│   └── jumia_and_konga_data3.csv  # Product data (price, ratings, etc.)
├── backend/
│   ├── models/
│   │   ├── main.py            # Data embedding (DataEmbedder) and recommendation logic (Recommender)
│   │   └── verify_chroma.py  # Optional ChromaDB verification script
│   └── vector_db/            # ChromaDB storage directory
├── .env                      # Environment variables (OPENAI_API_KEY)
├── requirements.txt          # Python dependencies
|── README.md                 # This file 
|__app.py # Streamlit web interface

**Prerequisites**
Python: 3.11

Dependencies: Listed in requirements.txt

API Key: OpenAI API key (stored in .env)

**Setup** 
*1. Clone the repository*
git clone https://github.com/IdowuAdamo/Neural-Drip.git
cd Neural-Drip

2. Create a Virtual Environment:
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

3. Install Dependencies:
pip install -r requirements.txt

4. Set Up Environment Variables:
Create a .env file in the root directory:
OPENAI_API_KEY=your_openai_api_key_here

5. Embed Data (Run Once): 
run the embedding code in main.py:
python backend/models/main.py
This processes the CSV, generates embeddings, and stores them in backend/vector_db/. Comment out afterward to avoid re-running.

6. Run the Streamlit App:
streamlit run backend/models/app.py

7. Contributing
Fork the repo, make changes, and submit a pull request to IdowuAdamo/Neural-Drip.
Report issues or suggest features via GitHub Issues.











