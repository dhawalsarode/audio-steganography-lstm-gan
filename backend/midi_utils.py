# backend/midi_utils.py
import mido
import base64
from utils.aes_utils import decrypt_message
from io import BytesIO

def midi_notes_to_bytes(notes: list) -> bytes:
    """Convert MIDI notes back to original bytes."""
    return bytes(notes)

def midi_to_message(midi_bytes: bytes, password: str) -> str:
    mid = mido.MidiFile(file=BytesIO(midi_bytes))
    notes = []

    for track in mid.tracks:
        for msg in track:
            if msg.type == 'note_on':
                notes.append(msg.note)

    # Convert back to base64 string
    encrypted_b64_bytes = midi_notes_to_bytes(notes)
    encrypted_b64 = encrypted_b64_bytes.decode("utf-8", errors="ignore")

    if not encrypted_b64.strip():
        raise ValueError("Extracted base64 is empty or invalid")

    return decrypt_message(encrypted_b64, password)
