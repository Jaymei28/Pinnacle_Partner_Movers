import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import loginImage from '../images/loginpic.png';
import usernameIcon from '../images/username.svg';
import passwordIcon from '../images/password.svg';

const LoginPage = ({ setIsLoggedIn }) => {
    const [loginData, setLoginData] = useState({ username: '', password: '' });
    const [loginError, setLoginError] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setLoginError('');
        setLoading(true);
        try {
            const response = await axios.post('http://localhost:8000/api/login/', loginData);
            localStorage.setItem('token', response.data.token);
            setIsLoggedIn(true);
            navigate('/dashboard');
        } catch (err) {
            setLoginError('Invalid username or password. Please try again.');
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
                                    type="password"
                                    placeholder="password"
                                    value={loginData.password}
                                    onChange={e => setLoginData({ ...loginData, password: e.target.value })}
                                    required
                                />
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
