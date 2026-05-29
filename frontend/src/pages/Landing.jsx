import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Landing.css';

const features = [
  {
    icon: '📄',
    title: 'Resume Analysis',
    description: 'AI-powered deep analysis of your resume structure, content, and formatting for maximum impact.',
  },
  {
    icon: '🎯',
    title: 'ATS Scoring',
    description: 'Get your Applicant Tracking System compatibility score and optimize for automated screening.',
  },
  {
    icon: '🎤',
    title: 'AI Mock Interview',
    description: 'Practice with AI-generated interview questions tailored to your experience and target role.',
  },
  {
    icon: '💻',
    title: 'Coding Tests',
    description: 'Sharpen your coding skills with curated problems and real-time code execution.',
  },
  {
    icon: '🧠',
    title: 'Skill Extraction',
    description: 'Automatically extract and categorize technical skills, frameworks, and competencies.',
  },
  {
    icon: '📊',
    title: 'Dashboard Analytics',
    description: 'Track your progress with beautiful charts and actionable insights over time.',
  },
];

const stats = [
  { value: '10,000+', label: 'Resumes Analyzed' },
  { value: '95%', label: 'Accuracy Rate' },
  { value: '50+', label: 'Skill Categories' },
  { value: '5,000+', label: 'Interviews Practiced' },
];

export default function Landing() {
  const { isAuthenticated } = useAuth();

  return (
    <div className="landing-page">
      {/* Navbar */}
      <header className="landing-nav">
        <div className="landing-nav-inner">
          <Link to="/" className="landing-logo">
            <span className="landing-logo-icon">⚡</span>
            <span className="landing-logo-text">Resume<span className="logo-highlight">AI</span></span>
          </Link>
          <nav className="landing-nav-links">
            <a href="#features" className="landing-nav-link">Features</a>
            <a href="#stats" className="landing-nav-link">Stats</a>
            {isAuthenticated ? (
              <Link to="/dashboard" className="btn btn-primary">Dashboard</Link>
            ) : (
              <div className="landing-nav-actions">
                <Link to="/login" className="btn btn-ghost">Sign In</Link>
                <Link to="/register" className="btn btn-primary">Get Started</Link>
              </div>
            )}
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-bg-effects">
          <div className="hero-gradient-orb hero-orb-1"></div>
          <div className="hero-gradient-orb hero-orb-2"></div>
        </div>
        <div className="hero-content">
          <div className="hero-badge">
            <span className="hero-badge-dot"></span>
            AI-Powered Career Platform
          </div>
          <h1 className="hero-title">
            Your AI-Powered<br />
            <span className="hero-title-highlight">Resume Analyzer</span>
          </h1>
          <p className="hero-subtitle">
            Get instant ATS scores, AI-driven resume analysis, mock interviews, and coding challenges — everything you need to land your dream job.
          </p>
          <div className="hero-actions">
            <Link to={isAuthenticated ? '/upload' : '/register'} className="btn btn-primary btn-lg">
              Get Started Free →
            </Link>
            <a href="#features" className="btn btn-outline btn-lg">
              Learn More
            </a>
          </div>
          <div className="hero-trusted">
            <p className="hero-trusted-label">Trusted by professionals worldwide</p>
            <div className="hero-stats-inline">
              <div className="hero-stat-inline">
                <span className="hero-stat-value">10K+</span>
                <span className="hero-stat-label">Users</span>
              </div>
              <div className="hero-stat-divider"></div>
              <div className="hero-stat-inline">
                <span className="hero-stat-value">95%</span>
                <span className="hero-stat-label">Accuracy</span>
              </div>
              <div className="hero-stat-divider"></div>
              <div className="hero-stat-inline">
                <span className="hero-stat-value">4.9★</span>
                <span className="hero-stat-label">Rating</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section" id="features">
        <div className="section-container">
          <div className="section-header">
            <span className="section-badge">Features</span>
            <h2 className="section-title">Everything you need to<br /><span className="title-accent">ace your job search</span></h2>
            <p className="section-subtitle">Powerful AI tools designed to give you a competitive edge in today's job market.</p>
          </div>
          <div className="features-grid">
            {features.map((feature, index) => (
              <div key={index} className="feature-card" style={{ animationDelay: `${index * 0.1}s` }}>
                <div className="feature-icon-wrapper">
                  <span className="feature-icon">{feature.icon}</span>
                </div>
                <h3 className="feature-title">{feature.title}</h3>
                <p className="feature-description">{feature.description}</p>
                <span className="feature-link">
                  Learn more
                  <span className="feature-arrow">→</span>
                </span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="stats-section" id="stats">
        <div className="section-container">
          <div className="stats-grid">
            {stats.map((stat, index) => (
              <div key={index} className="stat-item">
                <span className="stat-value">{stat.value}</span>
                <span className="stat-label">{stat.label}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="section-container">
          <div className="cta-card">
            <h2 className="cta-title">Ready to supercharge your career?</h2>
            <p className="cta-subtitle">Join thousands of professionals who trust ResumeAI for their career growth.</p>
            <div className="cta-actions">
              <Link to={isAuthenticated ? '/dashboard' : '/register'} className="btn btn-primary btn-lg cta-btn">
                Start Free Analysis →
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="landing-footer">
        <div className="section-container">
          <div className="footer-top">
            <div className="footer-brand-col">
              <div className="footer-brand">
                <span className="landing-logo-icon">⚡</span>
                <span className="landing-logo-text">Resume<span className="logo-highlight">AI</span></span>
              </div>
              <p className="footer-brand-desc">AI-powered career platform helping professionals land their dream jobs.</p>
            </div>
            <div className="footer-links-grid">
              <div className="footer-links-col">
                <h4 className="footer-col-title">Product</h4>
                <a href="#features" className="footer-link">Features</a>
                <Link to="/register" className="footer-link">Get Started</Link>
                <a href="#stats" className="footer-link">Stats</a>
              </div>
              <div className="footer-links-col">
                <h4 className="footer-col-title">Company</h4>
                <a href="#" className="footer-link">About</a>
                <a href="#" className="footer-link">Careers</a>
                <a href="#" className="footer-link">Contact</a>
              </div>
              <div className="footer-links-col">
                <h4 className="footer-col-title">Legal</h4>
                <a href="#" className="footer-link">Privacy</a>
                <a href="#" className="footer-link">Terms</a>
                <a href="#" className="footer-link">Security</a>
              </div>
            </div>
          </div>
          <div className="footer-bottom">
            <p className="footer-text">© 2026 ResumeAI. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
