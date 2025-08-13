# backend/generate.py
import mido
import os
import base64
from utils.aes_utils import encrypt_message

def bytes_to_midi_notes(byte_data: bytes) -> list:
    """Convert bytes to MIDI notes (0-127 range)."""
    return list(byte_data)  # each byte is already 0–255 but MIDI will mod it to 0–127

def generate_midi(secret_message: str, password: str, output_path: str = "output/output.mid"):
    # AES encrypt → base64 encode → bytes
    encrypted_b64 = encrypt_message(secret_message, password).encode("utf-8")

    # Map bytes to MIDI notes
    notes = bytes_to_midi_notes(encrypted_b64)

    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)

    for note in notes:
        midi_note = note % 128  # keep in MIDI range
        track.append(mido.Message('note_on', note=midi_note, velocity=64, time=0))
        track.append(mido.Message('note_off', note=midi_note, velocity=64, time=200))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    mid.save(output_path)
    print(f"[✅] Encrypted MIDI saved at: {output_path}")

if __name__ == "__main__":
    msg = input("Enter secret message: ")
    pwd = input("Enter password: ")
    generate_midi(msg, pwd)
