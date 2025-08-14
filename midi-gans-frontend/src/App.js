import React, { useState } from 'react';
import { ThemeProvider, createTheme, CssBaseline, IconButton } from '@mui/material';
import { LightMode, DarkMode } from '@mui/icons-material';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import Generate from './components/Generate';
import Decrypt from './components/Decrypt';

function App() {
  const [mode, setMode] = useState('light');

  const theme = createTheme({
    palette: {
      mode: mode,
      primary: { main: '#1976d2' },
      secondary: { main: '#9c27b0' },
    },
  });

  const toggleMode = () => setMode(prev => (prev === 'light' ? 'dark' : 'light'));

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 20px' }}>
        <h1>🎵 Audio Steganography Tool</h1>
        <IconButton onClick={toggleMode} color="inherit">
          {mode === 'light' ? <DarkMode /> : <LightMode />}
        </IconButton>
      </div>

      <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: 40, marginTop: 40 }}>
        <Generate />
        <Decrypt />
      </div>

      {/* Toast Container is global — shows messages from any component */}
      <ToastContainer position="bottom-right" autoClose={3000} />
    </ThemeProvider>
  );
}

export default App;
