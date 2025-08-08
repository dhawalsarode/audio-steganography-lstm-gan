# backend/app.py

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "<h2>🎵 Audio Steganography Backend is Running</h2><p>Use /generate, /encode, or /decode endpoints</p>"

@app.route('/generate', methods=['POST'])
def generate():
    # Placeholder logic for MIDI generation
    return jsonify({"status": "✅ MIDI file generated!"})

@app.route('/encode', methods=['POST'])
def encode():
    # Placeholder logic for encoding secret message
    return jsonify({"status": "✅ Secret message encoded into MIDI!"})

@app.route('/decode', methods=['POST'])
def decode():
    # Placeholder logic for decoding message
    return jsonify({"message": "🔓 This is your hidden message."})

if __name__ == '__main__':
    app.run(debug=True)
