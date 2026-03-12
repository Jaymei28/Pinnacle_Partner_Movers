import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { useLoader } from '../PageLoader';
import loginImage from '../images/loginpic.png';
import usernameIcon from '../images/username.svg';
import passwordIcon from '../images/password.svg';
import showIcon from '../images/showpass.png';
import hideIcon from '../images/hidepass.png';

const LoginPage = ({ setIsLoggedIn }) => {
    const [loginData, setLoginData] = useState({ username: '', password: '' });
    const [loginError, setLoginError] = useState('');
    const [loading, setLoading] = useState(false);
    const [showPassword, setShowPassword] = useState(false);
    const navigate = useNavigate();
    const { startLoading, stopLoading } = useLoader();

    const handleLogin = async (e) => {
        // ... previous handleLogin logic preserved ...
        e.preventDefault();
        setLoginError('');
        setLoading(true);
        startLoading();
        try {
            let VITE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
            if (VITE_URL && !VITE_URL.startsWith('http')) {
                VITE_URL = `https://${VITE_URL}`;
            }
            const API_BASE_URL = VITE_URL.endsWith('/api/') ? VITE_URL : `${VITE_URL.replace(/\/$/, '')}/api/`;
            const response = await axios.post(`${API_BASE_URL}login/`, loginData);
            localStorage.setItem('token', response.data.token);
            setIsLoggedIn(true);
            stopLoading();
            navigate('/dashboard');
        } catch (err) {
            setLoginError('Invalid username or password. Please try again.');
            stopLoading();
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-page-split">
            {/* Left Side - Company Logo Image */}
            <div className="login-image-section">
                <img src={loginImage} alt="Company Logo" />
            </div>

            {/* Right Side - Login Form */}
            <div className="login-form-section">
                <div className="login-form-container">
                    <div className="login-header">
                        <h2>Welcome</h2>
                        <p>Login to access dashboard</p>
                    </div>

                    <form onSubmit={handleLogin} className="login-form">
                        <div className="form-group">
                            <label>Username</label>
                            <div className="input-with-icon">
                                <img src={usernameIcon} alt="" className="input-icon" />
                                <input
                                    type="text"
                                    placeholder="username"
                                    value={loginData.username}
                                    onChange={e => setLoginData({ ...loginData, username: e.target.value })}
                                    required
                                />
                            </div>
                        </div>
                        <div className="form-group">
                            <label>Password</label>
                            <div className="input-with-icon">
                                <img src={passwordIcon} alt="" className="input-icon" />
                                <input
                                    type={showPassword ? "text" : "password"}
                                    placeholder="password"
                                    value={loginData.password}
                                    onChange={e => setLoginData({ ...loginData, password: e.target.value })}
                                    required
                                />
                                <button
                                    type="button"
                                    className="password-toggle-btn"
                                    onClick={() => setShowPassword(!showPassword)}
                                >
                                    <img src={showPassword ? hideIcon : showIcon} alt="Toggle Password" />
                                </button>
                            </div>
                        </div>

                        {loginError && <div className="error-msg">{loginError}</div>}

                        <button
                            type="submit"
                            className="btn-primary btn-login"
                            disabled={loading}
                        >
                            {loading ? 'Logging in...' : 'Sign In'}
                        </button>
                    </form>

                    <div className="login-footer">
                        <p>
                            Don't have an account? <a href="/" className="signup-link">Sign up</a>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default LoginPage;
