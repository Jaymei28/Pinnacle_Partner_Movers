import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';
import Opportunities from './pages/Opportunities';
import Carriers from './pages/Carriers';
import './index.css';

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem('token'));

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsLoggedIn(false);
  };

  return (
    <Router>
      <div className="app">
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={
            isLoggedIn ? <Navigate to="/dashboard" /> : <LandingPage />
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

            <Route path="settings" element={<div className="status-msg">Account and notification settings.</div>} />
          </Route>

          {/* Catch-all Redirect */}
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
