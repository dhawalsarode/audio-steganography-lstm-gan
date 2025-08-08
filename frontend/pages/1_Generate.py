import streamlit as st
import os
import streamlit as st
import os
import json

USER_FILE = os.path.join(os.path.dirname(__file__), "../users.json")

def is_logged_in():
    if not os.path.exists(USER_FILE):
        return False
    with open(USER_FILE, "r") as f:
        users = json.load(f)
    return "logged_in" in st.session_state and st.session_state.logged_in

if not is_logged_in():
    st.warning("Please log in to access this page.")
    st.stop()

st.title("🎵 Generate Encrypted MIDI")

# Show form
with st.form("generation_form"):
    secret_message = st.text_area("Enter your secret message", max_chars=200)
    password = st.text_input("Enter password", type="password")
    submit_button = st.form_submit_button("Generate")

if submit_button:
    if not secret_message or not password:
        st.warning("Please provide both a secret message and a password.")
    else:
        try:
            # Ensure backend is triggered with correct absolute path
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
            generate_script = os.path.join(project_root, 'backend', 'generate.py')
            
            command = f'python "{generate_script}" "{secret_message}" "{password}"'
            result = os.system(command)
            
            output_path = os.path.join(project_root, "output", "output.mid")

            if result == 0 and os.path.exists(output_path):
                st.success("✅ MIDI generated successfully!")
                with open(output_path, "rb") as f:
                    st.download_button("⬇️ Download MIDI File", f, file_name="encrypted_output.mid")
            else:
                st.error("❌ Failed to generate MIDI. Check logs.")
        except Exception as e:
            st.exception(e)
