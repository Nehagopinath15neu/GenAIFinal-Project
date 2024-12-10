import streamlit as st
import requests
import os

# Streamlit UI configuration
st.set_page_config(page_title="Customer Support Chatbot", page_icon="💬")
st.title("Customer Support Chatbot 💬")

# Backend URL
BACKEND_URL = "http://127.0.0.1:5000/process_ticket"

# Conversation history storage
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# User input for ticket description
user_query = st.text_area("Enter your ticket description:")

# Submit button
if st.button("Submit Ticket"):
    if user_query:
        # Send POST request to the backend
        try:
            response = requests.post(BACKEND_URL, json={"description": user_query})
            response_data = response.json()

            if response.status_code == 200:
                category = response_data.get("category", "Unknown Category")
                response_text = response_data.get("response", "No response generated.")

                # Store and display the conversation
                st.session_state.conversation_history.append(f"**User:** {user_query}")
                st.session_state.conversation_history.append(f"**Category:** {category}")
                st.session_state.conversation_history.append(f"**Response:** {response_text}")

                st.success("Ticket processed successfully!")
            else:
                st.error(response_data.get("error", "An error occurred."))

        except Exception as e:
            st.error(f"Error: {e}")

# Display conversation history
st.subheader("Conversation History")
for message in st.session_state.conversation_history:
    st.write(message)
