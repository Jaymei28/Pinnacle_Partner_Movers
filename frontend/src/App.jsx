import React, { useState } from 'react';
import { HashRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';
import Opportunities from './pages/Opportunities';
import Carriers from './pages/Carriers';
import Settings from './pages/Settings';
import { PageLoaderProvider } from './PageLoader';
import './index.css';

// Apply saved theme immediately on load (before first render) so it persists on refresh
const savedTheme = localStorage.getItem('theme') || 'light';
document.documentElement.setAttribute('data-theme', savedTheme);

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem('token'));

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsLoggedIn(false);
  };

  return (
    <PageLoaderProvider>
      <Router>
        <div className="app">
          <Routes>
            {/* Public Routes */}
            <Route path="/" element={
              isLoggedIn ? <Navigate to="/dashboard" /> : <LoginPage setIsLoggedIn={setIsLoggedIn} />
            } />

            <Route path="/login" element={
              isLoggedIn ? <Navigate to="/dashboard" /> : <LoginPage setIsLoggedIn={setIsLoggedIn} />
            } />

            {/* Protected Routes */}
            <Route path="/dashboard" element={
              isLoggedIn ? <Dashboard handleLogout={handleLogout} /> : <Navigate to="/login" />
            }>
              <Route index element={<Opportunities />} />

              <Route path="carriers" element={<Carriers />} />

              <Route path="settings" element={<Settings />} />
            </Route>

            {/* Catch-all Redirect */}
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </div>
      </Router>
    </PageLoaderProvider>
  );
};

export default App;
