import React, { useState, useEffect } from 'react';

const Settings = () => {
    const [theme, setTheme] = useState('light');

    // Load theme from localStorage on mount
    useEffect(() => {
        const savedTheme = localStorage.getItem('theme') || 'light';
        setTheme(savedTheme);
        document.documentElement.setAttribute('data-theme', savedTheme);
    }, []);

    // Toggle theme
    const toggleTheme = () => {
        const newTheme = theme === 'light' ? 'dark' : 'light';
        setTheme(newTheme);
        localStorage.setItem('theme', newTheme);
        document.documentElement.setAttribute('data-theme', newTheme);
    };

    return (
        <div className="opportunities-view">
            <div className="carriers-header">
                <h2>Settings</h2>
                <p className="carriers-subtitle">
                    Customize your experience and preferences.
                </p>
            </div>

            <div className="settings-container">
                {/* Theme Section */}
                <div className="settings-section">
                    <h3 className="settings-section-title">Appearance</h3>

                    <div className="settings-item">
                        <div className="settings-item-info">
                            <h4 className="settings-item-label">Theme</h4>
                            <p className="settings-item-description">
                                Choose between light and dark mode
                            </p>
                        </div>

                        <div className="theme-toggle-wrapper">
                            <button
                                className={`theme-option ${theme === 'light' ? 'active' : ''}`}
                                onClick={() => {
                                    if (theme !== 'light') toggleTheme();
                                }}
                            >
                                <svg className="theme-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                    <circle cx="12" cy="12" r="5" />
                                    <line x1="12" y1="1" x2="12" y2="3" />
                                    <line x1="12" y1="21" x2="12" y2="23" />
                                    <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
                                    <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
                                    <line x1="1" y1="12" x2="3" y2="12" />
                                    <line x1="21" y1="12" x2="23" y2="12" />
                                    <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
                                    <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
                                </svg>
                                Light
                            </button>

                            <button
                                className={`theme-option ${theme === 'dark' ? 'active' : ''}`}
                                onClick={() => {
                                    if (theme !== 'dark') toggleTheme();
                                }}
                            >
                                <svg className="theme-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                    <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
                                </svg>
                                Dark
                            </button>
                        </div>
                    </div>
                </div>

                {/* Current Theme Display */}
                <div className="settings-info-box">
                    <svg className="info-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <circle cx="12" cy="12" r="10" />
                        <line x1="12" y1="16" x2="12" y2="12" />
                        <line x1="12" y1="8" x2="12.01" y2="8" />
                    </svg>
                    <p>
                        Current theme: <strong>{theme === 'light' ? 'Light Mode' : 'Dark Mode'}</strong>
                        <br />
                        Your preference is saved and will persist across sessions.
                    </p>
                </div>
            </div>
        </div>
    );
};

export default Settings;
