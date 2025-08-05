# backend/generate.py

import mido
import os
from utils.aes_utils import encrypt_message

def message_to_notes(encrypted: str) -> list:
    """Convert base64 encrypted string to MIDI note values (integers)."""
    return [ord(c) % 128 for c in encrypted]  # MIDI note range: 0–127

def generate_midi(secret_message: str, password: str, output_path: str = "output/output.mid"):
    # Encrypt the message
    encrypted = encrypt_message(secret_message, password)

    # Map to notes
    notes = message_to_notes(encrypted)

    # Setup MIDI
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)

    # Add MIDI notes with fixed duration
    for note in notes:
        track.append(mido.Message('note_on', note=note, velocity=64, time=0))
        track.append(mido.Message('note_off', note=note, velocity=64, time=200))

    # Create output directory if not exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save MIDI file
    mid.save(output_path)
    print(f"[✅] Encrypted MIDI saved at: {output_path}")

# Example usage (for CLI testing)
if __name__ == "__main__":
    msg = input("Enter secret message: ")
    pwd = input("Enter password: ")
    generate_midi(msg, pwd)
