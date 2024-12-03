import openai
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# OpenAI API Key
openai.api_key = "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"

# MongoDB Connection URI
uri = "mongodb+srv://ashkarfrancis1:frafra45@cluster0.jbpov.mongodb.net/?retryWrites=true&w=majority"

# Initialize Flask App
app = Flask(__name__, template_folder="../templates")
CORS(app)

# Connect to MongoDB
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["jobs_db"]

# List of collections to search
collections_to_search = ["QA"]

def extract_keywords_with_openai(user_query):
    """
    Use OpenAI's GPT-4 API to extract relevant keywords and infer intent.
    Always include the original query words for single-word searches.
    """
    # Step 1: Ask GPT-4 to infer intent and extract keywords
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an advanced assistant that interprets user queries to extract keywords. "
                    "You can handle ambiguous, misspelled, or vague phrases, and infer their intent "
                    "(e.g., 'am still studying' -> 'student'). Always return relevant job-related terms."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Extract keywords or infer intent from this query: '{user_query}'. "
                    "Return them as a comma-separated list, preserving the original query words too."
                )
            }
        ],
        max_tokens=100,
        temperature=0.2,  # Low temperature for consistent results
    )
    gpt_keywords = response['choices'][0]['message']['content'].strip().split(", ")

    # Step 2: Include the original query words as keywords
    original_keywords = user_query.lower().split()  # Split the original query into words
    all_keywords = set(gpt_keywords).union(original_keywords)  # Combine into a set for uniqueness

    # Step 3: Check the database for matching terms
    # Example: Predefine known terms or fetch from the database
    known_roles = ["student", "developer", "intern", "engineer", "QA", "designer"]
    known_companies = ["Google", "Microsoft", "Amazon", "Apple", "Meta"]
    known_locations = ["New York", "San Francisco", "London", "Berlin", "Tel Aviv"]

    matched_keywords = []
    for keyword in all_keywords:
        keyword_lower = keyword.lower()

        # Match against known roles
        if any(role in keyword_lower for role in known_roles):
            matched_keywords.append(keyword)

        # Match against known companies
        if any(company.lower() in keyword_lower for company in known_companies):
            matched_keywords.append(keyword)

        # Match against known locations
        if any(location.lower() in keyword_lower for location in known_locations):
            matched_keywords.append(keyword)

    # Step 4: Combine GPT-4 results, database matches, and original words
    final_keywords = list(all_keywords.union(matched_keywords))  # Ensure uniqueness
    return final_keywords





@app.route("/")
def index():
    """
    Render the frontend HTML page.
    """
    return render_template("index.html")

@app.route("/search", methods=["GET"])
def search_jobs():
    """
    Endpoint to search for jobs based on a user's query.
    """
    query = request.args.get("query", "").strip()
    if not query:
        return jsonify({"error": "Query parameter is missing."}), 400

    # Extract keywords using OpenAI GPT
    keywords = extract_keywords_with_openai(query)
    if not keywords:
        return jsonify({"message": "No relevant keywords found in query."}), 400

    # Construct MongoDB regex query
    regex_query = {"$or": [
        {"role": {"$regex": "|".join(keywords), "$options": "i"}},
        {"company": {"$regex": "|".join(keywords), "$options": "i"}},
        {"location": {"$regex": "|".join(keywords), "$options": "i"}}
    ]}

    # Aggregate results from all collections
    all_results = []
    for collection_name in collections_to_search:
        collection = db[collection_name]
        results = collection.find(regex_query)
        for doc in results:
            all_results.append({
                "role": doc.get("role"),
                "company": doc.get("company"),
                "location": doc.get("location"),
                "time_posted": doc.get("time_posted"),
                "score": doc.get("score"),
                "links": doc.get("links")
            })

    return jsonify(all_results)

if __name__ == "__main__":
    app.run(debug=True)
