# backend/extract.py

import mido
from utils.aes_utils import decrypt_message

def notes_to_encrypted_string(notes: list) -> str:
    """Rebuild encrypted base64 string from MIDI notes (0–127)."""
    return ''.join([chr(n) for n in notes])

def extract_message(midi_file_path: str, password: str) -> str:
    mid = mido.MidiFile(midi_file_path)
    notes = []

    for msg in mid:
        if msg.type == 'note_on':
            notes.append(msg.note)

    encrypted = notes_to_encrypted_string(notes)

    try:
        decrypted = decrypt_message(encrypted, password)
        print(f"[✅] Extracted Message: {decrypted}")
        return decrypted
    except Exception as e:
        print(f"[❌] Decryption failed: {e}")
        return None

# Example usage
if __name__ == "__main__":
    midi_path = input("Enter path to MIDI file: ")
    pwd = input("Enter password: ")
    extract_message(midi_path, pwd)
