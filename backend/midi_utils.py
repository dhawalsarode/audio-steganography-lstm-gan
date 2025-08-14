import mido
import base64
from utils.aes_utils import decrypt_message
from io import BytesIO

def midi_notes_to_bytes(notes: list) -> bytes:
    """Convert MIDI notes (0–127) to raw bytes."""
    try:
        return bytes(notes)
    except ValueError as e:
        raise ValueError(f"Invalid note value in MIDI: {e}")

def midi_to_message(midi_bytes: bytes, password: str) -> str:
    mid = mido.MidiFile(file=BytesIO(midi_bytes))
    notes = []

    for track in mid.tracks:
        for msg in track:
            if msg.type == 'note_on' and 0 <= msg.note <= 127:
                notes.append(msg.note)

    if not notes:
        raise ValueError("No note_on events found in the MIDI file.")

    encrypted_b64_bytes = midi_notes_to_bytes(notes)
    encrypted_b64 = encrypted_b64_bytes.decode("utf-8", errors="ignore").strip()

    if not encrypted_b64:
        raise ValueError("Extracted base64 string is empty after decoding.")

    try:
        base64.b64decode(encrypted_b64, validate=True)
    except Exception as e:
        raise ValueError(f"Extracted data is not valid Base64: {e}")

    try:
        decrypted = decrypt_message(encrypted_b64, password)
        return decrypted
    except Exception as e:
        raise ValueError(f"Decryption failed: {type(e).__name__}: {e}")
