import mido
from utils.aes_utils import encrypt_message

START_MARKER = 0   # Valid MIDI note for start
END_MARKER = 1     # Valid MIDI note for end

def message_to_midi_notes(enc_str: str):
    return [ord(ch) for ch in enc_str]

def generate_midi(secret_message: str, password: str, output_path: str):
    enc_str = encrypt_message(secret_message, password)
    notes = [START_MARKER] + message_to_midi_notes(enc_str) + [END_MARKER]

    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)

    for note in notes:
        track.append(mido.Message('note_on', note=note if note <= 127 else 127, velocity=64, time=120))

    print(f"[DEBUG] Generated {len(notes)} notes with markers.")
    mid.save(output_path)
    return output_path
