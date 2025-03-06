import os 
from dotenv import load_dotenv
import chromadb
from openai import OpenAI

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize clients
client = OpenAI(api_key=openai_api_key)
chroma_client = chromadb.PersistentClient(path="backend/vector_db")
collection = chroma_client.get_collection(name="products")

def get_recommendations(query, budget, num_results):
    """
    Get product recommendations based on a query, budget, and desired number of results.
    
    Args:
        query (str): User search query (e.g., "affordable phone under ₦150,000")
        budget (float): Maximum price in Naira
        num_results (int): Number of products to return
    
    Returns:
        str: LLM-generated recommendation text
    """
    # Embed the query
    query_embedding = client.embeddings.create(input=query, model="text-embedding-ada-002").data[0].embedding

    # Query the vector DB (fetch more results to allow filtering)
    results = collection.query(query_embeddings=[query_embedding], n_results=10)

    # Filter by budget and limit to num_results
    filtered_results = [
        {"id": id, "metadata": meta, "document": doc}
        for id, meta, doc in zip(results["ids"][0], results["metadatas"][0], results["documents"][0])
        if meta["price_ngn"] <= budget
    ][:num_results]

    if not filtered_results:
        return "No products found within your budget matching your query."

    # Prepare context for LLM
    context = "\n".join([
        f"{r['document']} - Rating: {r['metadata']['rating']} - Link: {r['metadata']['url']}"
        for r in filtered_results
    ])
    prompt = (
        f"Given this product data:\n{context}\n"
        f"Recommend the best value-for-money option for a user looking for '{query}'. "
        f"Consider price, discount, and rating in your reasoning, and suggest alternatives if applicable."
    )

    # Query OpenAI LLM
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )

    return response.choices[0].message.content

# testing
if __name__ == "__main__":
    query = "affordable phone under ₦150,000"
    budget = 150_000
    num_results = 3
    recommendation = get_recommendations(query, budget, num_results)
    # Handle Unicode safely for printing
    try:
        print(recommendation)
    except UnicodeEncodeError:
        # Strip non-ASCII characters if terminal can't handle them
        safe_output = recommendation.encode("ascii", "ignore").decode("ascii")
        print(safe_output)