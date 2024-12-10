import os
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

app = Flask(__name__)

# Function to categorize a ticket using Groq API
def categorize_ticket(description):
    response = client.chat.completions.create(
        model="llama2-7b-70b",
        messages=[{"role": "user", "content": f"Categorize this support ticket: {description}"}],
        temperature=0.7,
        max_tokens=50
    )
    return response.choices[0].message.content.strip()

# Function to generate a response using Groq API
def generate_response(category, description):
    response = client.chat.completions.create(
        model="llama2-7b-70b",
        messages=[{"role": "user", "content": f"Generate a support response for a {category} issue: {description}"}],
        temperature=0.7,
        max_tokens=100
    )
    return response.choices[0].message.content.strip()

# Route to process the ticket
@app.route("/process_ticket", methods=["POST"])
def process_ticket():
    try:
        data = request.json
        description = data.get("description")
        if not description:
            return jsonify({"error": "Please provide a ticket description."}), 400

        category = categorize_ticket(description)
        response = generate_response(category, description)

        return jsonify({"category": category, "response": response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
