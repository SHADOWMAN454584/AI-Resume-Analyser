import { NavLink, useLocation } from 'react-router-dom';
import './Sidebar.css';

const navItems = [
  { path: '/dashboard', icon: '📊', label: 'Dashboard' },
  { path: '/upload', icon: '📤', label: 'Upload Resume' },
  { path: '/analysis', icon: '🔍', label: 'Analysis' },
  { path: '/interview', icon: '🎤', label: 'AI Interview' },
  { path: '/coding', icon: '💻', label: 'Coding Test' },
];

export default function Sidebar({ isOpen, onClose }) {
  const location = useLocation();

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && <div className="sidebar-overlay" onClick={onClose}></div>}

      <aside className={`sidebar ${isOpen ? 'sidebar-open' : ''}`}>
        {/* Logo */}
        <div className="sidebar-logo">
          <div className="logo-icon">⚡</div>
          <span className="logo-text">
            Resume<span className="logo-highlight">AI</span>
          </span>
        </div>

        {/* Navigation */}
        <nav className="sidebar-nav">
          <div className="sidebar-section-label">MAIN MENU</div>
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `sidebar-link ${isActive || location.pathname.startsWith(item.path) ? 'sidebar-link-active' : ''}`
              }
              onClick={onClose}
            >
              <span className="sidebar-link-icon">{item.icon}</span>
              <span className="sidebar-link-label">{item.label}</span>
              {location.pathname.startsWith(item.path) && <span className="sidebar-active-dot"></span>}
            </NavLink>
          ))}
        </nav>

        {/* Bottom section */}
        <div className="sidebar-footer">
          <div className="sidebar-upgrade-card">
            <div className="upgrade-icon">🚀</div>
            <p className="upgrade-title">Upgrade to Pro</p>
            <p className="upgrade-text">Unlock unlimited analysis & interviews</p>
            <button className="btn btn-primary btn-sm w-full">Upgrade</button>
          </div>
        </div>
      </aside>
    </>
  );
}
