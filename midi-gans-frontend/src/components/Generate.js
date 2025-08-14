import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import {
  Card, CardContent, Typography, TextField, Button,
  CircularProgress, MenuItem, FormControl, Select, InputLabel,
  Switch, FormControlLabel
} from '@mui/material';
import { toast } from 'react-toastify';
import { Midi } from '@tonejs/midi';
import Soundfont from 'soundfont-player';
import MidiVisualizer from './MidiVisualizer';

export default function Generate() {
  const [message, setMessage] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [midiData, setMidiData] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [instrument, setInstrument] = useState('acoustic_grand_piano');
  const [loop, setLoop] = useState(false);
  const [playTime, setPlayTime] = useState(0);

  const audioCtxRef = useRef(null);
  const playStartRef = useRef(null);
  const requestIdRef = useRef(null);

  const handleGenerate = async () => {
    setMidiData(null);
    if (!message || !password) {
      toast.error('⚠️ Please enter both a secret message and password.');
      return;
    }
    setLoading(true);
    try {
      const response = await axios.post('/generate', { message, password });
      setMidiData(response.data.file);
      toast.success('✅ MIDI file generated successfully!');
    } catch (err) {
      toast.error(err.response?.data?.error || '❌ Failed to generate MIDI');
    } finally {
      setLoading(false);
    }
  };

  const downloadMidi = () => {
    const link = document.createElement('a');
    link.href = `data:audio/midi;base64,${midiData}`;
    link.download = 'secret.mid';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const stopPlayback = () => {
    if (audioCtxRef.current) {
      audioCtxRef.current.close().catch(() => {});
      audioCtxRef.current = null;
      setIsPlaying(false);
      setPlayTime(0);
      if (requestIdRef.current) {
        cancelAnimationFrame(requestIdRef.current);
        requestIdRef.current = null;
      }
      toast.info('⏹ Playback stopped');
    }
  };

  useEffect(() => {
    if (!isPlaying) {
      setPlayTime(0);
      if (requestIdRef.current) {
        cancelAnimationFrame(requestIdRef.current);
        requestIdRef.current = null;
      }
      return;
    }
    playStartRef.current = performance.now();

    const update = (timestamp) => {
      const elapsed = (timestamp - playStartRef.current) / 1000;
      setPlayTime(elapsed);
      requestIdRef.current = requestAnimationFrame(update);
    };
    requestIdRef.current = requestAnimationFrame(update);

    return () => {
      if (requestIdRef.current) {
        cancelAnimationFrame(requestIdRef.current);
        requestIdRef.current = null;
      }
    };
  }, [isPlaying]);

  const playMidi = async () => {
    if (!midiData) return;

    try {
      const midi = new Midi(
        new Uint8Array(atob(midiData).split('').map(c => c.charCodeAt(0)))
      );

      // stop old playback
      stopPlayback();

      const audioContext = new (window.AudioContext || window.webkitAudioContext)();
      audioCtxRef.current = audioContext;
      const player = await Soundfont.instrument(audioContext, instrument);

      setIsPlaying(true);

      const scheduleNotes = () => {
        midi.tracks.forEach(track => {
          track.notes.forEach(note => {
            player.play(note.name, audioContext.currentTime + note.time, {
              duration: note.duration,
              gain: note.velocity
            });
          });
        });
      };

      scheduleNotes();

      if (loop) {
        const totalMs = midi.duration * 1000;
        const intervalId = setInterval(() => {
          if (!audioCtxRef.current) {
            clearInterval(intervalId);
            return;
          }
          playStartRef.current = performance.now();
          scheduleNotes();
        }, totalMs);
      } else {
        setTimeout(() => {
          setIsPlaying(false);
          audioCtxRef.current = null;
        }, midi.duration * 1000);
      }
    } catch (err) {
      toast.error('❌ Could not play MIDI');
      console.error(err);
    }
  };

  return (
    <Card sx={{ width: 500 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Generate Encrypted MIDI
        </Typography>

        <TextField
          multiline
          fullWidth
          rows={4}
          label="Secret Message"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          sx={{ mb: 2 }}
        />

        <TextField
          fullWidth
          type="password"
          label="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          sx={{ mb: 2 }}
        />

        <FormControl fullWidth sx={{ mb: 2 }}>
          <InputLabel>Instrument</InputLabel>
          <Select
            value={instrument}
            label="Instrument"
            onChange={(e) => setInstrument(e.target.value)}
          >
            <MenuItem value="acoustic_grand_piano">🎹 Piano</MenuItem>
            <MenuItem value="violin">🎻 Violin</MenuItem>
            <MenuItem value="flute">🎶 Flute</MenuItem>
            <MenuItem value="electric_guitar_clean">🎸 Electric Guitar</MenuItem>
            <MenuItem value="xylophone">🪘 Xylophone</MenuItem>
            <MenuItem value="acoustic_guitar_nylon">🎼 Nylon Guitar</MenuItem>
            <MenuItem value="trumpet">🎺 Trumpet</MenuItem>
          </Select>
        </FormControl>

        <FormControlLabel
          control={
            <Switch
              checked={loop}
              onChange={(e) => setLoop(e.target.checked)}
              color="primary"
            />
          }
          label="Loop Playback"
          sx={{ mb: 2 }}
        />

        <Button
          variant="contained"
          color="primary"
          onClick={handleGenerate}
          disabled={loading}
          fullWidth
          sx={{ mb: 2 }}
        >
          {loading ? <CircularProgress size={24} /> : 'Generate MIDI'}
        </Button>

        {midiData && (
          <>
            <Button
              variant="outlined"
              color="secondary"
              onClick={downloadMidi}
              fullWidth
              sx={{ mb: 1 }}
            >
              Download MIDI
            </Button>
            <Button
              variant="outlined"
              color={isPlaying ? 'success' : 'primary'}
              onClick={playMidi}
              disabled={isPlaying && !loop}
              fullWidth
              sx={{ mb: 1 }}
            >
              {isPlaying ? (loop ? 'Looping...' : 'Playing...') : '🎵 Play MIDI'}
            </Button>
            <Button
              variant="outlined"
              color="error"
              onClick={stopPlayback}
              disabled={!isPlaying}
              fullWidth
              sx={{ mb: 2 }}
            >
              ⏹ Stop
            </Button>

            {/* MIDI Visualizer */}
            <MidiVisualizer midiBase64={midiData} playTime={playTime} />
          </>
        )}
      </CardContent>
    </Card>
  );
}
