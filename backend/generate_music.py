def generate_dummy_midi():
    # This simulates saving a MIDI file
    with open("static/plots/generated.mid", "wb") as f:
        f.write(b"MThd\x00\x00\x00\x06\x00\x01\x00\x01\x00\x60MTrk\x00\x00\x00\x04\x00\xFF\x2F\x00")
    return "static/plots/generated.mid"
