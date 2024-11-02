import requests
import streamlit as st
import numpy as np
import random
import time
import os

# Initialize assistant response
assistant_response = "Error communicating with a server"

# Define API URL and directory path
API_URL = "http://localhost:8000"
directoryPath = r"D:\@Ehab_Training\@RAG\Code\NaiveRAG\Vector_Store"

# Check if the vector store directory is empty and initialize the model
if not os.listdir(directoryPath):
    if "model_Initialize" not in st.session_state:
        with st.spinner("Initiate the Project"):
            response = requests.post(url=f"{API_URL}/Init_model", timeout=400)
            print(response)
            st.session_state.model_Initialize = True

st.title("Naive RAG Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

    # List of welcome messages
    welcome_messages = [
        "حياك الله , شو بتحب تسأل 👀",
        "مرحبا كيف بتحب نساعدك"
    ]

    # Append a random welcome message
    first_message = random.choice(welcome_messages)
    st.session_state.messages.append({"role": "assistant", "content": first_message})

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input for the prompt
if prompt := st.chat_input("What is up?"):
    with st.chat_message("user"):
        st.markdown(prompt)

    # Store user prompt in session state
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Send the query to the API
    response = requests.post(f"{API_URL}/query", json={"query": prompt})

    if response.status_code == 200:
        assistant_response = response.json().get("response", "Sorry, I couldn't process that.")
    else:
        assistant_response = "Error communicating with a server"

    # Display assistant's response
    with st.chat_message("assistant"):
        # Display the entire response at once instead of word by word
        st.markdown(assistant_response)

    # Append assistant response to messages
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
