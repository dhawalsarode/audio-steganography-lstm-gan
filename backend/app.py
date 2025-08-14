# backend/app.py
import sys
import os

# Add the project root directory to sys.path so imports work
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.generate import generate_midi
from backend.extract import extract_message

import os
import base64
from flask import Flask, request, jsonify, send_file
from backend.generate import generate_midi
from backend.extract import extract_message

app = Flask(__name__)

@app.route('/')
def home():
    return "<h2>🎵 Audio Steganography Backend is Running</h2><p>Use /generate or /decode endpoints.</p>"

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        message = data.get("message")
        password = data.get("password")

        if not message or not password:
            return jsonify({"error": "Message and password are required"}), 400

        output_path = "generated.mid"
        generate_midi(message, password, output_path)

        # Send the MIDI file as base64 so the frontend can save it
        with open(output_path, "rb") as f:
            midi_b64 = base64.b64encode(f.read()).decode("utf-8")

        return jsonify({
            "status": "✅ MIDI file generated!",
            "file": midi_b64
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/decode', methods=['POST'])
def decode():
    try:
        midi_file = request.files.get("file")
        password = request.form.get("password")

        if not midi_file or not password:
            return jsonify({"error": "MIDI file and password are required"}), 400

        temp_path = "temp.mid"
        midi_file.save(temp_path)

        message = extract_message(temp_path, password)

        return jsonify({
            "status": "✅ Message extracted!",
            "message": message
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

