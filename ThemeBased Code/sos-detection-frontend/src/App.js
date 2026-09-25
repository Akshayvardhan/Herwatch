import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material';
import Layout from './components/Layout';
import Login from './pages/Login';
import Register from './pages/Register';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import LiveCamera from './pages/LiveCamera';
import VideoMode from './pages/VideoMode';
import HotspotMap from './pages/HotspotMap';
import Profile from './pages/Profile';
import About from './pages/About';

// 🌈 Custom Material UI theme
const theme = createTheme({
  palette: {
    primary: {
      main: '#1a237e', // Dark blue
    },
    secondary: {
      main: '#f50057', // Pink
    },
    background: {
      default: '#f5f5f5', // Light gray background
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h4: { fontWeight: 600 },
    h5: { fontWeight: 600 },
    h6: { fontWeight: 600 },
  },
});

// 🔒 PrivateRoute for future authentication feature
// eslint-disable-next-line no-unused-vars
const PrivateRoute = ({ children }) => {
  const isAuthenticated = true; // TODO: Replace with actual auth check
  return isAuthenticated ? children : <Navigate to="/login" />;
};

const App = () => {
  // 🧠 Side effect to set browser title once app loads
  useEffect(() => {
    document.title = "HerWatch – Women Safety Application by Akshay";
    console.log("🚀 HerWatch App initialized successfully!");
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Routes>
          {/* Public Routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Main Layout Routes */}
          <Route path="/" element={<Layout />}>
            <Route index element={<Home />} />
            <Route path="about" element={<About />} />
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="live-camera" element={<LiveCamera />} />
            <Route path="video-mode" element={<VideoMode />} />
            <Route path="hotspot-map" element={<HotspotMap />} />
            <Route path="profile" element={<Profile />} />
          </Route>
        </Routes>
      </Router>
    </ThemeProvider>
  );
};

export default App;
