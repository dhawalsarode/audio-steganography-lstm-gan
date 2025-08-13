import streamlit as st
import os
import json
import sys

USER_FILE = os.path.join(os.path.dirname(__file__), "../users.json")

def is_logged_in():
    return "authenticated" in st.session_state and st.session_state["authenticated"]

if not is_logged_in():
    st.warning("Please log in to access this page.")
    st.stop()

# Add backend folder to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../backend")))

from utils.aes_utils import decrypt_message
from midi_utils import midi_to_message
from io import BytesIO

st.title("🔓 Decrypt Secret Message from MIDI")
st.markdown("Upload an encrypted `.mid` file and provide the password to extract the hidden message.")

uploaded_file = st.file_uploader("📂 Upload Encrypted MIDI File", type=["mid", "midi"])
password = st.text_input("🔑 Enter Decryption Password", type="password")

if st.button("Decrypt"):
    if uploaded_file and password:
        try:
            midi_bytes = uploaded_file.read()
            decrypted = midi_to_message(midi_bytes, password)

            st.success("✅ Message Decrypted:")
            st.code(decrypted)

        except Exception as e:
            st.error(f"❌ Failed to decrypt: {str(e)}")
    else:
        st.warning("Please upload a file and enter the password.")