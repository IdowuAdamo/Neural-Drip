import os
from dotenv import load_dotenv
import chromadb
from openai import OpenAI

# load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# initialize clients
client = OpenAI(api_key=openai_api_key)
chroma_client = chromadb.PersistentClient(path="backend/vector_db")
collection = chroma_client.get_collection(name="products")

def get_recommendations(query, budget, num_results):
    """
    Get product recommendations based on a query, budget, and desired number of results.
    
    Args:
        query (str): User search query (e.g., "affordable phone under ₦80,000")
        budget (float): Maximum price in Naira
        num_results (int): Number of products to return
    
    Returns:
        str: LLM-generated recommendation text
    """
    # embed the query
    query_embedding = client.embeddings.create(input=query, model="text-embedding-ada-002").data[0].embedding

    # query the vector DB
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
        f"- Product: {r['document']}, Rating: {r['metadata']['rating']}, Link: {r['metadata']['url']}"
        for r in filtered_results
    ])

    # Prompt for structured output
    prompt = (
        f"You are an expert shopping assistant. Given this product data:\n{context}\n"
        f"Recommend the best value-for-money option for '{query}' within a budget of ₦{budget}. "
        f"Consider price, discount, and rating. Provide exactly {num_results} recommendations if available, "
        f"each with a clear explanation of why it’s a good choice. Include alternatives if applicable. "
        f"Format your response as a numbered list with this structure for each item:\n"
        f"X. **Product Name** - Price: ₦XXX - Discount: XX% - Rating: X.X\n"
        f"   - Reason: [Why it’s recommended]\n"
        f"   - Link: <a href='[URL]'>Buy Now</a>\n"
        f"Do not recommend products exceeding the budget of ₦{budget}. "
        f"If fewer than {num_results} items are available, explain why."
    )

    # Query OpenAI LLM
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024  # increased from 200 to 1024
    )

    return response.choices[0].message.content

# testing
if __name__ == "__main__":
    query = "affordable phone under ₦80,000"
    budget = 80000
    num_results = 3
    recommendation = get_recommendations(query, budget, num_results)
    try:
        print(recommendation)
    except UnicodeEncodeError:
        safe_output = recommendation.encode("ascii", "ignore").decode("ascii")
        print(safe_output)