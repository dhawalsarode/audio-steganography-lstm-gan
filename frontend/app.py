# frontend/app.py

import streamlit as st
from streamlit_option_menu import option_menu
import os

st.set_page_config(page_title="Audio Steganography", layout="centered")

# -- Fake login (for demo) --
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.title("🔐 Audio Steganography Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username and password:
            st.session_state.logged_in = True
            st.success("Logged in!")
        else:
            st.error("Please enter both username and password.")

if not st.session_state.logged_in:
    login()
else:
    # Sidebar navigation
    with st.sidebar:
        selected = option_menu(
            menu_title="Navigation",
            options=["Home", "Generate", "Decrypt"],
            icons=["house", "music-note-beamed", "lock-open"],
            default_index=0,
        )

    if selected == "Home":
        st.title("🎵 Welcome to Audio Steganography")
        st.write("Securely hide and retrieve secret messages inside MIDI files using GANs + AES encryption.")

    elif selected == "Generate":
        st.switch_page("pages/1_Generate.py")

    elif selected == "Decrypt":
        st.switch_page("pages/2_Decrypt.py")
