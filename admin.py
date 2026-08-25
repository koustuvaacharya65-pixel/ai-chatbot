import streamlit as st
from dotenv import load_dotenv
import os

from database import get_conversations, get_messages, delete_conversation

# ==========================================
# LOAD LOCAL .ENV
# ==========================================

load_dotenv()


# ==========================================
# GET PASSWORD FROM STREAMLIT CLOUD OR .ENV
# ==========================================

def get_secret(name):
    try:
        return st.secrets[name]
    except Exception:
        return os.getenv(name, "")


# ==========================================
# ADMIN ACCOUNTS
# ==========================================

admins = {
    "admin1": get_secret("ADMIN1_PASSWORD"),
    "admin2": get_secret("ADMIN2_PASSWORD"),
    "admin3": get_secret("ADMIN3_PASSWORD"),
    "admin4": get_secret("ADMIN4_PASSWORD"),
    "admin5": get_secret("ADMIN5_PASSWORD"),
    "admin6": get_secret("ADMIN6_PASSWORD")
}


# ==========================================
# PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="Admin Panel",
    page_icon="🔐",
    layout="wide"
)


# ==========================================
# LOGIN SESSION
# ==========================================

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if "admin_username" not in st.session_state:
    st.session_state.admin_username = ""


# ==========================================
# LOGIN PAGE
# ==========================================

if not st.session_state.admin_logged_in:

    st.title("🔐 Admin Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login", type="primary"):

        if username in admins and password == admins[username]:

            st.session_state.admin_logged_in = True
            st.session_state.admin_username = username

            st.rerun()

        else:

            st.error("Incorrect username or password.")

    st.stop()


# ==========================================
# ADMIN DASHBOARD
# ==========================================

st.title("🛠️ Admin Dashboard")

st.write(
    f"Logged in as: **{st.session_state.admin_username}**"
)


# ==========================================
# LOGOUT
# ==========================================

if st.button("Logout"):

    st.session_state.admin_logged_in = False
    st.session_state.admin_username = ""

    st.rerun()


st.divider()


# ==========================================
# CHAT HISTORY
# ==========================================

st.subheader("💬 Chat History")

conversations = get_conversations()


if not conversations:

    st.info("No conversations found.")

else:

    for conversation in conversations:

        conversation_id = conversation[0]
        title = conversation[1]
        created_at = conversation[2]

        with st.expander(
            f"💬 {title} | {created_at}"
        ):

            messages = get_messages(conversation_id)

            if messages:

                for role, content in messages:

                    if role == "user":

                        st.markdown(
                            f"**User:** {content}"
                        )

                    else:

                        st.markdown(
                            f"**AI:** {content}"
                        )

            else:

                st.write("No messages.")

            st.divider()

            if st.button(
                "🗑️ Delete conversation",
                key=f"delete_{conversation_id}"
            ):

                delete_conversation(conversation_id)

                st.success(
                    "Conversation deleted."
                )

                st.rerun()