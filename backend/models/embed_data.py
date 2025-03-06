import csv
import os
from dotenv import load_dotenv
import chromadb
from openai import OpenAI

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

# Load and preprocess CSV data
products = []
with open("data\jumia_phone.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            price = float(row["price"].replace("₦ ", "").replace(",", ""))
            rating_str = row["ratings"]
            rating = float(rating_str.split(" out of ")[0]) if rating_str and "out of" in rating_str else None
            discount = float(row["discount"].replace("%", "")) / 100 if row["discount"] and "%" in row["discount"] else 0.0
            
            # Skip rows with missing or invalid ratings
            if rating is None:
                # Use encode to handle Unicode characters safely
                safe_name = row["product_name"].encode("ascii", "ignore").decode("ascii")
                print(f"Skipping row with missing/invalid rating: {safe_name}")
                continue

            products.append({
                "product_name": row["product_name"],
                "price_ngn": price,
                "discount": discount,
                "rating": rating,
                "product_link": row["product_link"]
            })
        except (ValueError, KeyError) as e:
            safe_name = row["product_name"].encode("ascii", "ignore").decode("ascii")
            print(f"Error processing row {safe_name}: {str(e)}")
            continue
        except UnicodeEncodeError as e:
            safe_name = row["product_name"].encode("ascii", "ignore").decode("ascii")
            print(f"Unicode error in row {safe_name}: {str(e)}")
            continue

# Initialize Chroma client
chroma_client = chromadb.PersistentClient(path="backend/vector_db")
collection = chroma_client.get_or_create_collection(name="products")

# Prepare data for embedding
texts = [f"{p['product_name']} - ₦{p['price_ngn']} - Discount: {p['discount']*100}%" for p in products]
ids = [f"prod_{i}" for i in range(len(products))]
metadatas = [
    {"price_ngn": p["price_ngn"], "discount": p["discount"], "rating": p["rating"], "url": p["product_link"]}
    for p in products
]

# Generate embeddings
response = client.embeddings.create(input=texts, model="text-embedding-ada-002")
embeddings = [r.embedding for r in response.data]

# Store in Chroma
collection.add(
    embeddings=embeddings,
    documents=texts,
    metadatas=metadatas,
    ids=ids
)

print(f"Data embedded and stored in vector DB! {len(products)} products processed.")