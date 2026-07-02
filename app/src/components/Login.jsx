import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const BASE = (process.env.REACT_APP_API_URL || '').replace(/['"]/g, '');

export default function Login() {
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    async function handleSubmit(e) {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            const res = await fetch(`${BASE}/api/token/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password }),
            });

            if (!res.ok) {
                const data = await res.json().catch(() => ({}));
                throw new Error(data?.detail || 'Invalid credentials');
            }

            const { access, refresh } = await res.json();
            localStorage.setItem('access_token', access);
            localStorage.setItem('refresh_token', refresh);
            navigate('/home');
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="login-page">
            <div className="login-card">
                <div className="login-brand">
                    <span className="login-brand-dot" />
                    <span className="login-brand-name">perpend</span>
                </div>

                <h1 className="login-heading">Welcome back</h1>
                <p className="login-sub">Sign in to continue your learning roadmap.</p>

                <form className="login-form" onSubmit={handleSubmit} noValidate>
                    <div className="login-field">
                        <label htmlFor="login-username" className="login-label">Username</label>
                        <input
                            id="login-username"
                            type="text"
                            className="login-input"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            autoComplete="username"
                            autoFocus
                            required
                        />
                    </div>

                    <div className="login-field">
                        <label htmlFor="login-password" className="login-label">Password</label>
                        <input
                            id="login-password"
                            type="password"
                            className="login-input"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            autoComplete="current-password"
                            required
                        />
                    </div>

                    {error && (
                        <p className="login-error" role="alert">{error}</p>
                    )}

                    <button
                        id="login-submit"
                        type="submit"
                        className={`login-btn${loading ? ' login-btn--loading' : ''}`}
                        disabled={loading}
                    >
                        {loading ? <span className="login-spinner" /> : 'Sign in'}
                    </button>
                </form>
            </div>
        </div>
    );
}