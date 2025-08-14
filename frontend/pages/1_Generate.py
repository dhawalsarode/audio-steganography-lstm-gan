import sys
import os

# Ensure project root is in PYTHONPATH so backend package can be imported
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from backend.generate import generate_midi
import streamlit as st

st.title("Generate Encrypted MIDI")

secret_message = st.text_area("Secret Message")
password = st.text_input("Password", type="password")

if st.button("Generate MIDI"):
    if not secret_message or not password:
        st.error("Please enter both a secret message and a password.")
    else:
        try:
            output_path = os.path.join(ROOT_DIR, "output.mid")
            generate_midi(secret_message, password, output_path)
            with open(output_path, "rb") as f:
                st.download_button("Download MIDI", f, file_name="secret.mid", mime="audio/midi")
            st.success("MIDI file generated successfully!")
        except Exception as e:
            st.error(f"Error generating MIDI: {e}")
