import streamlit as st
import requests

# Streamlit UI configuration
st.set_page_config(page_title="Customer Support Chatbot", page_icon="💬")
st.title("Welcome to CSYE 7380 - Final Project")
st.title("Customer Support Chatbot 💬")

# Conversation history storage
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# Input fields
user_query = st.text_area("Enter your support ticket description:")
model_name = st.selectbox("Choose Model:", ["gemma-7b-it", "llama3-8b-8192"])
use_rag = st.checkbox("Enable RAG Mode")

# Button to send the query
if st.button("Submit Ticket"):
    if user_query:
        with st.spinner("Processing your ticket..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:5000/process_ticket",
                    json={"description": user_query, "model": model_name, "use_rag": use_rag}
                )
                if response.status_code == 200:
                    data = response.json()
                    category = data["category"]
                    reply = data["response"]

                    # Display the response
                    st.subheader("Category:")
                    st.write(category)

                    st.subheader("Response:")
                    st.write(reply)

                    # Store the conversation
                    st.session_state.conversation_history.append(f"**You:** {user_query}")
                    st.session_state.conversation_history.append(f"**Bot:** {reply}")

                    # Store the current query and response for feedback submission
                    st.session_state.latest_query = user_query
                    st.session_state.latest_model = model_name
                    st.session_state.latest_reply = reply

                else:
                    st.error(f"Error: {response.json().get('error', 'Unknown error occurred')}")

            except Exception as e:
                st.error(f"An error occurred: {e}")

# Display conversation history
st.subheader("Conversation History")
for message in st.session_state.conversation_history:
    st.write(message)

# Feedback section
if "latest_query" in st.session_state:
    st.subheader("Rate the Response")
    rating = st.radio("Rate the quality of this response:", [1, 2, 3, 4, 5], index=4)
    feedback_text = st.text_area("Additional feedback (optional):")

    if st.button("Submit Feedback"):
        try:
            feedback_response = requests.post(
                "http://127.0.0.1:5000/submit_feedback",
                json={
                    "description": st.session_state.latest_query,
                    "model": st.session_state.latest_model,
                    "rating": rating,
                    "feedback": feedback_text
                }
            )

            if feedback_response.status_code == 200:
                st.success("Thank you for your feedback!")
                # Optionally clear the feedback form after submission
                del st.session_state["latest_query"]
                del st.session_state["latest_model"]
                del st.session_state["latest_reply"]
            else:
                st.error("Failed to submit feedback.")

        except Exception as e:
            st.error(f"An error occurred: {e}")
