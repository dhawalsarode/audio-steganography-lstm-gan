from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "<h2>Audio Steganography Backend is running!</h2>"

@app.route('/generate', methods=['POST'])
def generate():
    return jsonify({"status": "MIDI file generated!"})

@app.route('/encode', methods=['POST'])
def encode():
    return jsonify({"status": "Message encoded!"})

@app.route('/decode', methods=['POST'])
def decode():
    return jsonify({"message": "This is a hidden message"})

if __name__ == '__main__':
    app.run(debug=True)
