import streamlit as st
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

# Admin accounts
admins = {
    "admin1": os.getenv("ADMIN1_PASSWORD"),
    "admin2": os.getenv("ADMIN2_PASSWORD"),
    "admin3": os.getenv("ADMIN3_PASSWORD"),
    "admin4": os.getenv("ADMIN4_PASSWORD"),
    "admin5": os.getenv("ADMIN5_PASSWORD"),
    "admin6": os.getenv("ADMIN6_PASSWORD")
}

st.set_page_config(
    page_title="Admin Login",
    page_icon="🔐"
)

st.title("🔐 Admin Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):

    if username in admins and password == admins[username]:

        st.success("Login successful!")

        st.subheader("Welcome to the Admin Panel")

        st.write(f"Logged in as: {username}")

    else:

        st.error("Incorrect username or password.")