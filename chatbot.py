import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

from database import (
    create_tables,
    create_conversation,
    save_message,
    get_conversations,
    get_messages,
    delete_conversation
)

# Load environment variables
load_dotenv()

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key)

# Create database tables
create_tables()

# Page settings
st.set_page_config(
    page_title="My AI Chatbot",
    page_icon="🤖"
)

# -----------------------------
# SESSION STATE
# -----------------------------

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.title("💬 Chat History")


# New Chat button
if st.sidebar.button("＋ New Chat"):

    st.session_state.conversation_id = None
    st.session_state.messages = []

    st.rerun()


# -----------------------------
# PREVIOUS CONVERSATIONS
# -----------------------------

conversations = get_conversations()

for conversation in conversations:

    conversation_id = conversation[0]
    title = conversation[1]

    col1, col2 = st.sidebar.columns([4, 1])

    # Open conversation
    with col1:

        if st.button(
            f"🗨️ {title}",
            key=f"conversation_{conversation_id}"
        ):

            st.session_state.conversation_id = conversation_id

            saved_messages = get_messages(conversation_id)

            st.session_state.messages = []

            for role, content in saved_messages:

                st.session_state.messages.append({
                    "role": role,
                    "content": content
                })

            st.rerun()


    # Delete conversation
    with col2:

        if st.button(
            "🗑️",
            key=f"delete_{conversation_id}"
        ):

            delete_conversation(conversation_id)

            if st.session_state.conversation_id == conversation_id:

                st.session_state.conversation_id = None
                st.session_state.messages = []

            st.rerun()


# -----------------------------
# MAIN CHAT
# -----------------------------

st.title("🤖 My AI Chatbot")

st.write("Ask me anything!")


# Display messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# Chat input
message = st.chat_input("Type your message here...")


if message:

    # Create a new conversation
    if st.session_state.conversation_id is None:

        title = message[:40]

        conversation_id = create_conversation(title)

        st.session_state.conversation_id = conversation_id


    # Save user's message
    save_message(
        st.session_state.conversation_id,
        "user",
        message
    )


    # Add user message to session
    st.session_state.messages.append({
        "role": "user",
        "content": message
    })


    # Display user message
    with st.chat_message("user"):
        st.write(message)


    # Build conversation for Gemini
    conversation_text = ""

    for msg in st.session_state.messages:

        conversation_text += (
            f"{msg['role']}: {msg['content']}\n"
        )


    # Ask Gemini
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=conversation_text
    )

    answer = response.text


    # Save AI response
    save_message(
        st.session_state.conversation_id,
        "assistant",
        answer
    )


    # Add AI response to session
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })


    # Display AI response
    with st.chat_message("assistant"):
        st.write(answer)