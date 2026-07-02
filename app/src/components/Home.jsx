import React, { useState, useEffect, useCallback, useRef } from 'react';
import { useNavigate } from 'react-router-dom';

const PALETTE = [
    '#FF0052', '#FFD400', '#00C68D', '#0055DA',
    '#5B7E3C', '#FFD65A', '#FF9D23', '#EA5252',
    '#202940', '#4B4038', '#9A8678', '#CAAA98',
];

function hexToRgb(hex) {
    const h = hex.replace('#', '');
    return {
        r: parseInt(h.substring(0, 2), 16),
        g: parseInt(h.substring(2, 4), 16),
        b: parseInt(h.substring(4, 6), 16),
    };
}

function relativeLuminance({ r, g, b }) {
    const sRGB = [r, g, b].map((c) => {
        const s = c / 255;
        return s <= 0.04045 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * sRGB[0] + 0.7152 * sRGB[1] + 0.0722 * sRGB[2];
}

function textColorFor(hex) {
    const lum = relativeLuminance(hexToRgb(hex));
    return lum > 0.35 ? '#1a1a1a' : '#ffffff';
}

const BASE = process.env.REACT_APP_API_URL;

function getToken() {
    return localStorage.getItem('access_token');
}

async function apiFetch(path, options = {}) {
    const token = getToken();
    const res = await fetch(`${BASE}${path}`, {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            ...(token ? { Authorization: `Bearer ${token}` } : {}),
            ...(options.headers || {}),
        },
    });
    if (res.status === 401) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        throw new Error('401');
    }
    if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
    return res.json();
}

export default function Home() {
    const navigate = useNavigate();
    const [roadmap, setRoadmap] = useState([]);
    const [activeId, setActiveId] = useState(null);
    const [completed, setCompleted] = useState(new Set());
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [menuOpen, setMenuOpen] = useState(false);
    const navRef = useRef(null);

    const makeKey = (topicId, subtopic) => `${topicId}::${subtopic}`;

    useEffect(() => {
        if (!getToken()) {
            navigate('/login');
            return;
        }

        let cancelled = false;

        async function init() {
            try {
                const [roadmapData, completedData] = await Promise.all([
                    apiFetch('/api/roadmap/'),
                    apiFetch('/api/todos/completed/'),
                ]);
                if (cancelled) return;

                setRoadmap(roadmapData);
                setActiveId(roadmapData[0]?.id ?? null);

                const doneSet = new Set(
                    completedData.map(({ topic_id, subtopic }) => makeKey(topic_id, subtopic))
                );
                setCompleted(doneSet);
            } catch (err) {
                if (!cancelled) {
                    if (err.message === '401') {
                        navigate('/login');
                    } else {
                        setError(err.message);
                    }
                }
            } finally {
                if (!cancelled) setLoading(false);
            }
        }

        init();
        return () => { cancelled = true; };
    }, [navigate]);

    useEffect(() => {
        function handleOutsideClick(e) {
            if (menuOpen && navRef.current && !navRef.current.contains(e.target)) {
                setMenuOpen(false);
            }
        }
        document.addEventListener('mousedown', handleOutsideClick);
        document.addEventListener('touchstart', handleOutsideClick);
        return () => {
            document.removeEventListener('mousedown', handleOutsideClick);
            document.removeEventListener('touchstart', handleOutsideClick);
        };
    }, [menuOpen]);

    const handleDoubleClick = useCallback(async (topicId, subtopic) => {
        const key = makeKey(topicId, subtopic);
        setCompleted((prev) => {
            const next = new Set(prev);
            if (next.has(key)) next.delete(key);
            else next.add(key);
            return next;
        });

        try {
            const result = await apiFetch('/api/todos/toggle/', {
                method: 'POST',
                body: JSON.stringify({ topic_id: topicId, subtopic }),
            });
            setCompleted((prev) => {
                const next = new Set(prev);
                if (result.completed) next.add(key);
                else next.delete(key);
                return next;
            });
        } catch (err) {
            if (err.message === '401') {
                navigate('/login');
            } else {
                setCompleted((prev) => {
                    const next = new Set(prev);
                    if (next.has(key)) next.delete(key);
                    else next.add(key);
                    return next;
                });
            }
        }
    }, [navigate]);

    const activeTopic = roadmap.find((t) => t.id === activeId);
    const doneCount = activeTopic
        ? activeTopic.subtopics.filter((s) => completed.has(makeKey(activeId, s.name))).length
        : 0;

    if (loading) {
        return (
            <div className="state-container">
                <div className="spinner" />
                <span>Loading roadmap…</span>
            </div>
        );
    }

    if (error) {
        return (
            <div className="state-container">
                <span>⚠ {error}</span>
            </div>
        );
    }

    return (
        <>
            <nav className="navbar" role="navigation" aria-label="Topics" ref={navRef}>
                <div className="navbar-left">
                    <span className="navbar-brand-dot" />
                    <span className="navbar-brand-name">perpend</span>
                </div>

                <button
                    className="navbar-toggle"
                    onClick={() => setMenuOpen(!menuOpen)}
                    aria-label="Toggle menu"
                    aria-expanded={menuOpen}
                >
                    <i className={menuOpen ? "fa-solid fa-xmark" : "fa-solid fa-bars"} />
                </button>

                <div className={`navbar-menu${menuOpen ? ' open' : ''}`}>
                    {roadmap.map((topic) => (
                        <button
                            key={topic.id}
                            id={`nav-topic-${topic.id}`}
                            className={`nav-item${topic.id === activeId ? ' active' : ''}`}
                            onClick={() => {
                                setActiveId(topic.id);
                                setMenuOpen(false);
                            }}
                            aria-current={topic.id === activeId ? 'page' : undefined}
                        >
                            {topic.topic}
                        </button>
                    ))}
                </div>

                <div className="navbar-progress-bar" aria-hidden="true">
                    <div
                        className="navbar-progress-fill"
                        style={{
                            width: `${activeTopic ? (doneCount / activeTopic.subtopics.length) * 100 : 0}%`
                        }}
                    />
                </div>
            </nav>

            <main className="page-container">
                {activeTopic && (
                    <>
                        <header className="topic-header">
                            <h1 className="topic-title">{activeTopic.topic}</h1>
                            <p className="topic-subtitle">
                                {doneCount} / {activeTopic.subtopics.length} completed
                                &nbsp;·&nbsp; double-click a box to mark it done
                            </p>
                        </header>

                        <div
                            className="subtopics-grid"
                            role="list"
                            aria-label={`${activeTopic.topic} subtopics`}
                        >
                            {activeTopic.subtopics.map((subtopic, idx) => {
                                const bg = PALETTE[idx % PALETTE.length];
                                const fg = textColorFor(bg);
                                const isDone = completed.has(makeKey(activeId, subtopic.name));

                                const pad = (n) => String(n).padStart(2, '0');
                                const serial = `${pad(activeId)}.${pad(idx + 1)}.XX`;

                                return (
                                    <div
                                        key={subtopic.name}
                                        id={`subtopic-${activeId}-${idx}`}
                                        role="listitem"
                                        className={`subtopic-box${isDone ? ' completed' : ''}`}
                                        style={{ backgroundColor: bg, color: fg }}
                                        onDoubleClick={() => handleDoubleClick(activeId, subtopic.name)}
                                        title={isDone ? 'Double-click to mark incomplete' : 'Double-click to mark complete'}
                                        aria-label={`${subtopic.name}${isDone ? ' (completed)' : ''}`}
                                    >
                                        <span className="subtopic-serial">{serial}</span>
                                        <i className={`${subtopic.icon} subtopic-icon`} aria-hidden="true" />
                                        {subtopic.name}
                                    </div>
                                );
                            })}
                        </div>
                    </>
                )}
            </main>
        </>
    );
}