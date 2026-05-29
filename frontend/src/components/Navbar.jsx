import { useState, useRef, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Navbar.css';

export default function Navbar({ onToggleSidebar }) {
  const { user, logout } = useAuth();
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [notifOpen, setNotifOpen] = useState(false);
  const dropdownRef = useRef(null);
  const notifRef = useRef(null);
  const navigate = useNavigate();
  const location = useLocation();

  // Close dropdowns on outside click
  useEffect(() => {
    const handleClick = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) setDropdownOpen(false);
      if (notifRef.current && !notifRef.current.contains(e.target)) setNotifOpen(false);
    };
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, []);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const getPageTitle = () => {
    const map = {
      '/dashboard': 'Dashboard',
      '/upload': 'Upload Resume',
      '/analysis': 'Resume Analysis',
      '/interview': 'AI Interview',
      '/coding': 'Coding Test',
    };
    return map[location.pathname] || 'Dashboard';
  };

  // Determine back navigation target
  const getBackTarget = () => {
    if (location.pathname === '/dashboard') return null; // No back on dashboard
    if (location.pathname === '/upload') return '/dashboard';
    if (location.pathname.startsWith('/analysis')) return '/dashboard';
    if (location.pathname === '/interview') return '/dashboard';
    if (location.pathname === '/coding') return '/dashboard';
    return '/dashboard';
  };

  const backTarget = getBackTarget();
  const initials = user?.username ? user.username.slice(0, 2).toUpperCase() : 'U';

  return (
    <nav className="navbar">
      <div className="navbar-left">
        <button className="navbar-toggle" onClick={onToggleSidebar} aria-label="Toggle sidebar">
          ☰
        </button>

        {/* Back Button */}
        {backTarget && (
          <button
            className="navbar-back-btn"
            onClick={() => navigate(backTarget)}
            aria-label="Go back"
          >
            <span className="back-arrow">←</span>
          </button>
        )}

        {/* Logo / Home Link */}
        <Link to="/dashboard" className="navbar-logo-link">
          <span className="navbar-logo-icon">⚡</span>
          <span className="navbar-logo-text">Resume<span className="navbar-logo-highlight">AI</span></span>
        </Link>

        <div className="navbar-divider-vertical"></div>
        <h1 className="navbar-title">{getPageTitle()}</h1>
      </div>

      <div className="navbar-right">
        {/* Notifications */}
        <div className="navbar-notif-wrapper" ref={notifRef}>
          <button className="navbar-icon-btn" onClick={() => setNotifOpen(!notifOpen)} aria-label="Notifications">
            🔔
            <span className="notif-dot"></span>
          </button>
          {notifOpen && (
            <div className="navbar-dropdown notif-dropdown">
              <div className="dropdown-header">
                <span className="dropdown-title">Notifications</span>
                <button className="dropdown-action">Mark all read</button>
              </div>
              <div className="dropdown-body">
                <div className="notif-item">
                  <span className="notif-icon">📄</span>
                  <div>
                    <p className="notif-text">Resume analysis complete</p>
                    <span className="notif-time">2 min ago</span>
                  </div>
                </div>
                <div className="notif-item">
                  <span className="notif-icon">🎯</span>
                  <div>
                    <p className="notif-text">New coding challenge available</p>
                    <span className="notif-time">1 hour ago</span>
                  </div>
                </div>
                <div className="notif-item">
                  <span className="notif-icon">✅</span>
                  <div>
                    <p className="notif-text">Interview score: 85/100</p>
                    <span className="notif-time">3 hours ago</span>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* User dropdown */}
        <div className="navbar-user-wrapper" ref={dropdownRef}>
          <button className="navbar-user-btn" onClick={() => setDropdownOpen(!dropdownOpen)}>
            <div className="navbar-avatar">{initials}</div>
            <span className="navbar-username hide-mobile">{user?.username || 'User'}</span>
            <span className="navbar-chevron">{dropdownOpen ? '▲' : '▼'}</span>
          </button>
          {dropdownOpen && (
            <div className="navbar-dropdown user-dropdown">
              <div className="dropdown-user-info">
                <div className="navbar-avatar navbar-avatar-lg">{initials}</div>
                <div>
                  <p className="dropdown-user-name">{user?.username || 'User'}</p>
                  <p className="dropdown-user-email">{user?.email || ''}</p>
                </div>
              </div>
              <div className="dropdown-divider"></div>
              <Link to="/dashboard" className="dropdown-item" onClick={() => setDropdownOpen(false)}>
                📊 Dashboard
              </Link>
              <Link to="/upload" className="dropdown-item" onClick={() => setDropdownOpen(false)}>
                📤 Upload Resume
              </Link>
              <div className="dropdown-divider"></div>
              <button className="dropdown-item dropdown-item-danger" onClick={handleLogout}>
                🚪 Logout
              </button>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}
