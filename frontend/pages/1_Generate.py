# frontend/pages/1_Generate.py

import streamlit as st
import subprocess
import os
from pathlib import Path

st.title("🔐 Embed Secret Message into MIDI")
st.markdown("Securely hide a message inside a MIDI file using LSTM-GAN and AES encryption.")

# Input fields
secret = st.text_area("Enter Secret Message", height=100)
password = st.text_input("Enter Password (for encryption)", type="password")

# Output path
output_path = Path("output/output.mid")

if st.button("Generate Encrypted MIDI"):
    if not secret or not password:
        st.error("Both message and password are required.")
    else:
        # Run backend/generate.py via subprocess
        result = subprocess.run(
            ["python", "backend/generate.py"],
            input=f"{secret}\n{password}\n",
            capture_output=True,
            text=True
        )

        if result.returncode == 0 and output_path.exists():
            st.success("✅ MIDI file generated and encrypted successfully!")
            with open(output_path, "rb") as f:
                st.download_button("🎵 Download Encrypted MIDI", f, file_name="secret_output.mid")
        else:
            st.error("❌ Failed to generate MIDI. Check logs.")
            st.code(result.stderr or result.stdout)
