import mido
import base64
from utils.aes_utils import decrypt_message

START_MARKER = 0
END_MARKER = 1

def extract_message(midi_file_path: str, password: str):
    mid = mido.MidiFile(midi_file_path)

    notes = []
    recording = False
    for msg in mid:
        if msg.type == 'note_on':
            if msg.note == START_MARKER:
                recording = True
                continue
            elif msg.note == END_MARKER:
                break
            elif recording and 0 <= msg.note <= 127:
                notes.append(msg.note)

    if not notes:
        raise ValueError("No encrypted data found in MIDI — start/end markers missing.")

    enc_str = ''.join(chr(n) for n in notes).strip()

    try:
        base64.b64decode(enc_str, validate=True)
    except Exception:
        raise ValueError("Extracted data is not valid Base64 — possible corruption or wrong file")

    return decrypt_message(enc_str, password)
