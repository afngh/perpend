import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function NotFound() {
    const navigate = useNavigate();

    return (
        <div className="notfound-page">
            <div className="notfound-code">404</div>
            <h1 className="notfound-heading">Page not found</h1>
            <p className="notfound-sub">
                The page you're looking for doesn't exist or was moved.
            </p>
            <button
                id="notfound-back"
                className="notfound-btn"
                onClick={() => navigate('/home')}
            >
                Back to home
            </button>
        </div>
    );
}