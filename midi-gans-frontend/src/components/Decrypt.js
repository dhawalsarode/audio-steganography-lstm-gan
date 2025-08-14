import React, { useState } from 'react';
import axios from 'axios';
import { Card, CardContent, Typography, TextField, Button, CircularProgress, Alert } from '@mui/material';
import { toast } from 'react-toastify';

export default function Decrypt() {
  const [file, setFile] = useState(null);
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleDecrypt = async () => {
    setMessage('');

    if (!file || !password) {
      toast.error('⚠️ Please upload a MIDI file and enter a password.');
      return;
    }

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('password', password);

      const response = await axios.post('/decode', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      setMessage(response.data.message);
      toast.success('✅ Message decrypted successfully!');
    } catch (err) {
      toast.error(err.response?.data?.error || '❌ Wrong password or invalid file');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card sx={{ width: 400 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Decrypt MIDI
        </Typography>

        <Button
          variant="outlined"
          component="label"
          fullWidth
          sx={{ mb: 2 }}
        >
          {file ? `Selected: ${file.name}` : 'Upload MIDI File'}
          <input
            type="file"
            accept=".mid,.midi"
            hidden
            onChange={(e) => setFile(e.target.files[0])}
          />
        </Button>

        <TextField
          fullWidth
          type="password"
          label="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          sx={{ mb: 2 }}
        />

        <Button
          variant="contained"
          color="primary"
          onClick={handleDecrypt}
          disabled={loading}
          fullWidth
          sx={{ mb: 2 }}
        >
          {loading ? <CircularProgress size={24} /> : 'Decrypt Message'}
        </Button>

        {message && (
          <Alert severity="success">
            <strong>Decrypted Message:</strong> {message}
          </Alert>
        )}
      </CardContent>
    </Card>
  );
}
