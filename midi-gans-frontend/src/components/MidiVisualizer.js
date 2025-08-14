import React, { useEffect, useRef, useState } from 'react';
import { Box, Typography } from '@mui/material';
import { Midi } from '@tonejs/midi';

const NOTE_HEIGHT = 10;    // Height of each note block in pixels
const PIANO_RANGE = 88;    // Number of piano keys (A0 to C8)
const KEYBOARD_LOWEST_NOTE = 21; // MIDI number for A0 (lowest piano key)
const PIXELS_PER_SECOND = 100;   // Horizontal scrolling speed

function MidiVisualizer({ midiBase64, playTime }) {
  const [midi, setMidi] = useState(null);
  const containerRef = useRef();

  useEffect(() => {
    if (!midiBase64) {
      setMidi(null);
      return;
    }

    // Parse the base64 MIDI data to a Midi object
    try {
      const midiData = new Midi(
        new Uint8Array(atob(midiBase64).split('').map(c => c.charCodeAt(0)))
      );
      setMidi(midiData);
    } catch (err) {
      console.error('Error parsing MIDI for visualization:', err);
      setMidi(null);
    }
  }, [midiBase64]);

  // Calculate scroll position based on current play time
  useEffect(() => {
    if (!containerRef.current || playTime == null) return;

    // Scroll visualization horizontally to keep playhead centered or visible
    const scrollX = playTime * PIXELS_PER_SECOND;
    containerRef.current.scrollLeft = scrollX;
  }, [playTime]);

  // Render note rectangles positioned by time and pitch
  const renderNotes = () => {
    if (!midi) return null;

    // We'll map MIDI note numbers (21 to 108 for piano range) vertically,
    // with A0 (21) at bottom and C8 (108) at top, so invert pitch axis.

    return midi.tracks.flatMap((track, trackIdx) =>
      track.notes.map((note, idx) => {
        const noteMidi = note.midi;
        // Y coordinate: position from bottom, invert Y for visualization
        const y = (PIANO_RANGE - (noteMidi - KEYBOARD_LOWEST_NOTE)) * NOTE_HEIGHT;

        // X coordinate is note start time * pixels per second
        const x = note.time * PIXELS_PER_SECOND;

        // Width based on note duration
        const width = Math.max(note.duration * PIXELS_PER_SECOND, 5);

        // Color can differ by track (use a set of preset colors)
        const colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'];
        const color = colors[trackIdx % colors.length];

        // If noteMidi is outside piano range, skip rendering
        if (noteMidi < KEYBOARD_LOWEST_NOTE || noteMidi > KEYBOARD_LOWEST_NOTE + PIANO_RANGE)
          return null;

        return (
          <rect
            key={`${trackIdx}-${idx}`}
            x={x}
            y={y}
            width={width}
            height={NOTE_HEIGHT - 1}
            fill={color}
            rx={2}
            ry={2}
          />
        );
      })
    );
  };

  if (!midi) {
    return <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
      No MIDI loaded for visualization.
    </Typography>;
  }

  // Visualization container width: enough to show entire MIDI duration plus some margin
  const containerWidth = Math.max(midi.duration * PIXELS_PER_SECOND + 300, 500);
  const containerHeight = PIANO_RANGE * NOTE_HEIGHT;

  return (
    <Box
      sx={{
        border: '1px solid',
        borderColor: 'divider',
        overflowX: 'auto',
        overflowY: 'hidden',
        height: containerHeight + 20,
        mt: 3,
        backgroundColor: 'background.paper',
        position: 'relative',
        whiteSpace: 'nowrap',
      }}
      ref={containerRef}
    >
      <svg
        width={containerWidth}
        height={containerHeight}
        style={{ display: 'block' }}
      >
        {/* Horizontal baseline or keyboard labels can be added here if desired */}

        {/* Render all notes */}
        {renderNotes()}

        {/* Playhead line */}
        {typeof playTime === 'number' && (
          <line
            x1={playTime * PIXELS_PER_SECOND}
            y1={0}
            x2={playTime * PIXELS_PER_SECOND}
            y2={containerHeight}
            stroke="#FF0000"
            strokeWidth={2}
            pointerEvents="none"
          />
        )}
      </svg>
    </Box>
  );
}

export default MidiVisualizer;
