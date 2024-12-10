import json
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from groq import Groq
import warnings
from urllib3.exceptions import NotOpenSSLWarning

# Suppress OpenSSL warnings
warnings.filterwarnings("ignore", category=NotOpenSSLWarning)

# Load environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=api_key)

app = Flask(__name__)

# Load sample ticket data
try:
    with open("sample_tickets.json", "r") as file:
        tickets = json.load(file)
except FileNotFoundError:
    tickets = []

# Function to categorize a ticket using the selected model
def categorize_ticket(description, model, use_rag=False):
    prompt = f"Categorize this support ticket: {description}"
    if use_rag:
        prompt = f"Use RAG to categorize this support ticket: {description}"

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50
    )
    category = response.choices[0].message.content.strip()
    return category

# Function to generate a response using the selected model
def generate_response(category, description, model, use_rag=False):
    prompt = f"Generate a support response for a {category} issue: {description}"
    if use_rag:
        prompt = f"Use RAG to generate a support response for a {category} issue: {description}"

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )
    response_text = response.choices[0].message.content.strip()
    return response_text

@app.route("/process_ticket", methods=["POST"])
def process_ticket():
    data = request.get_json()
    description = data.get("description")
    model = data.get("model")
    use_rag = data.get("use_rag", False)

    if not description:
        return jsonify({"error": "Please provide a ticket description."}), 400

    try:
        # Categorize the ticket and generate a response
        category = categorize_ticket(description, model, use_rag)
        response = generate_response(category, description, model, use_rag)

        return jsonify({"category": category, "response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/submit_feedback", methods=["POST"])
def submit_feedback():
    feedback_data = request.get_json()
    feedback_file = "feedback.json"

    try:
        # Check if the file exists and contains valid JSON
        if os.path.exists(feedback_file):
            with open(feedback_file, "r") as file:
                try:
                    feedback_list = json.load(file)
                except json.JSONDecodeError:
                    feedback_list = []  # Initialize with an empty list if the file is corrupted
        else:
            feedback_list = []

        # Add the new feedback
        feedback_list.append(feedback_data)

        # Save the updated feedback list
        with open(feedback_file, "w") as file:
            json.dump(feedback_list, file, indent=4)

        return jsonify({"message": "Feedback submitted successfully."})

    except Exception as e:
        # Log the exception for debugging
        print(f"Error saving feedback: {e}")
        return jsonify({"error": f"Failed to save feedback: {e}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
