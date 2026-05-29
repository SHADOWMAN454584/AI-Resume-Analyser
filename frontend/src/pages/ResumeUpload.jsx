import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { resumeAPI } from '../api/api';
import FileUpload from '../components/FileUpload';
import './ResumeUpload.css';

export default function ResumeUpload() {
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetchResumes();
  }, []);

  const fetchResumes = async () => {
    try {
      const res = await resumeAPI.list();
      setResumes(res.data.resumes || res.data || []);
    } catch (err) {
      console.error('Failed to fetch resumes:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleFileSelect = async (file) => {
    setUploading(true);
    setProgress(0);
    setError('');

    try {
      const res = await resumeAPI.upload(file, (progressEvent) => {
        const pct = Math.round((progressEvent.loaded * 100) / progressEvent.total);
        setProgress(Math.min(pct, 95));
      });

      setProgress(100);
      const resumeId = res.data?.resume?.id || res.data?.resume_id || res.data?.id;

      setTimeout(() => {
        if (resumeId) {
          navigate(`/analysis/${resumeId}`);
        } else {
          navigate('/dashboard'); // fallback
        }
      }, 800);
    } catch (err) {
      setError(err.response?.data?.message || err.response?.data?.error || 'Upload failed. Please try again.');
      setUploading(false);
      setProgress(0);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this resume?')) return;
    try {
      await resumeAPI.delete(id);
      setResumes((prev) => prev.filter((r) => r.id !== id));
    } catch (err) {
      console.error('Delete failed:', err);
    }
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return '';
    return new Date(dateStr).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  return (
    <div className="upload-page page-enter">
      {/* Back to Dashboard */}
      <Link to="/dashboard" className="back-btn">
        <span className="back-arrow">←</span> Back to Dashboard
      </Link>

      <div className="upload-header">
        <h2 className="upload-title">Upload Resume</h2>
        <p className="upload-subtitle">Upload your resume for AI-powered analysis and ATS scoring</p>
      </div>

      {error && (
        <div className="auth-error" style={{ marginBottom: 'var(--space-lg)' }}>
          <span>⚠️</span> {error}
        </div>
      )}

      <div className="upload-dropzone-section">
        <FileUpload onFileSelect={handleFileSelect} uploading={uploading} progress={progress} />
      </div>

      {/* Recent Uploads */}
      <div className="recent-uploads-section">
        <h3 className="section-title-sm">Recent Uploads</h3>
        {loading ? (
          <div className="loading-container">
            <div className="spinner"></div>
            <p>Loading resumes...</p>
          </div>
        ) : resumes.length === 0 ? (
          <div className="empty-state">
            <div className="empty-state-icon">📭</div>
            <p className="empty-state-title">No resumes yet</p>
            <p className="empty-state-text">Upload your first resume to get started with AI analysis</p>
          </div>
        ) : (
          <div className="resume-list">
            {resumes.map((resume) => (
              <div key={resume.id} className="resume-list-item glass-card">
                <div className="resume-item-icon">📄</div>
                <div className="resume-item-info">
                  <p className="resume-item-name">{resume.filename || resume.name || 'Resume'}</p>
                  <p className="resume-item-date">{formatDate(resume.created_at || resume.uploaded_at)}</p>
                </div>
                <div className="resume-item-score">
                  {resume.ats_score !== undefined && (
                    <span className={`score-badge ${resume.ats_score >= 70 ? 'score-good' : resume.ats_score >= 40 ? 'score-mid' : 'score-low'}`}>
                      {resume.ats_score}%
                    </span>
                  )}
                </div>
                <div className="resume-item-actions">
                  <button
                    className="btn btn-ghost btn-sm"
                    onClick={() => navigate(`/analysis/${resume.id}`)}
                  >
                    View
                  </button>
                  <button
                    className="btn btn-ghost btn-sm"
                    onClick={() => handleDelete(resume.id)}
                    style={{ color: 'var(--color-error)' }}
                  >
                    ✕
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
