import sys
import os

# Ensure project root is in PYTHONPATH so backend package can be imported
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from backend.extract import extract_message
import streamlit as st

st.title("Decrypt MIDI File")

uploaded_file = st.file_uploader("Upload MIDI", type=["mid", "midi"])
password = st.text_input("Password", type="password")

if st.button("Decrypt Message"):
    if not uploaded_file or not password:
        st.error("Please upload a MIDI file and enter a password.")
    else:
        try:
            temp_path = os.path.join(ROOT_DIR, "temp_uploaded.mid")
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.read())

            msg = extract_message(temp_path, password)
            st.success(f"Decrypted message: {msg}")
        except Exception as e:
            st.error(f"❌ Failed to decrypt: {e}")
