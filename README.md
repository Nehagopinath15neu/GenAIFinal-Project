# CSYE 7380 - Final Project Documentation: Simplified Digital Twin for a Customer Support System💬

## Project Overview 📖

This project implements a simplified digital twin for a customer support ticketing system using an LLM (Large Language Model). The system receives, categorizes, and responds to support tickets, leveraging an LLM to automate tasks typically requiring human intervention.

## Features 🚀

- **Ticket Categorization**: Automatically categorizes support tickets.
- **Response Generation**: Generates initial responses based on the ticket category.
- **RAG Integration**: Option to use Retrieval-Augmented Generation (RAG) for enhanced responses.
- **Feedback Mechanism**: Collects user feedback to improve response quality.

## Technologies Used 🛠️

- **Backend**: Flask
- **Frontend**: Streamlit
- **Models**: Gemma-7b-it, LLaMA3-8b-8192
- **API**: Groq API
- **Environment**: Python 3.9, dotenv for environment variables

## Installation Instructions 💻

```bash
git clone <[your-repo-url](https://github.com/Nehagopinath15neu/GenAIFinal-Project)>
cd <"/Users/nehagopinath/Documents/Courses /GenAI/Assignment 2"> <cd GenAI_Finalproject_neha> <source myenv/bin/activate> <cd src>

Create and Activate a Virtual Environment
- python3 -m venv myenv
- source myenv/bin/activate  

Install Dependencies
- pip install -r requirements.txt

Set Up Environment Variables
- GROQ_API_KEY=<your-groq-api-key>

 Run the Project
- python run_chatbot.py

Access the Frontend
- http://localhost:8501

Usage Instructions 📝
- Enter your support ticket description.
- Select a model (e.g., gemma-7b-it, llama3-8b-8192).
- Enable RAG mode if you want enhanced responses.
- Submit the ticket and receive a categorized response.
- Provide feedback to improve the system.

Project Structure 📂

project-root/
│-- app.py               # Flask backend
│-- frontend.py          # Streamlit frontend
│-- run_chatbot.py       # Script to run both frontend and backend
│-- requirements.txt     # List of dependencies
│-- sample_tickets.json  # Sample ticket data
│-- feedback.json        # Stores user feedback
└── .env                 # Environment variables (GROQ API key)


youtube link - https://youtu.be/tzClwyW-xiA


Future Enhancements ✨
- Add SLA tracking and priority levels.
- Simulate customer responses and escalations.
- Integrate with real ticketing system APIs.
- Improve LLM responses based on feedback loops.
