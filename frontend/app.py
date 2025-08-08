# frontend/app.py

import streamlit as st
import json
import os

st.set_page_config(page_title="Audio Steganography Login", page_icon="🔐", layout="centered")

USER_FILE = "frontend/users.json"

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_user(username, password):
    users = load_users()
    
    # ✅ Ensure frontend/ folder exists
    os.makedirs(os.path.dirname(USER_FILE), exist_ok=True)

    users[username] = password
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

def check_credentials(username, password):
    users = load_users()
    return username in users and users[username] == password

def login_screen():
    st.markdown("## 🔐 Audio Steganography Login")

    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])

    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            if check_credentials(username, password):
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.rerun()
            else:
                st.error("Invalid username or password")

    with tab2:
        new_username = st.text_input("Username", key="register_user")
        new_password = st.text_input("Password", type="password", key="register_pass")

        if st.button("Register"):
            if new_username and new_password:
                save_user(new_username, new_password)
                st.success("Registered successfully! Please login.")
            else:
                st.warning("Username and password cannot be empty.")

def main_app():
    st.sidebar.success(f"Logged in as: {st.session_state['username']}")
    st.markdown("# 🎵 Audio Steganography")
    st.write("Welcome to the secure music-based steganography app.")

    st.info("👉 Use the sidebar to navigate to **Generate** or **Decrypt** sections.")

# 🔐 App entrypoint
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login_screen()
else:
    main_app()
