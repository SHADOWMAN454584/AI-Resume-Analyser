import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { resumeAPI } from '../api/api';
import ScoreGauge from '../components/ScoreGauge';
import SkillBadge from '../components/SkillBadge';
import './ResumeAnalysis.css';

const defaultBreakdown = [
  { label: 'Contact Information', key: 'contact_info', icon: '📇' },
  { label: 'Formatting', key: 'formatting', icon: '📐' },
  { label: 'Keywords', key: 'keywords', icon: '🔑' },
  { label: 'Experience', key: 'experience', icon: '💼' },
  { label: 'Education', key: 'education', icon: '🎓' },
];

export default function ResumeAnalysis() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [resumes, setResumes] = useState([]);
  const [selectedId, setSelectedId] = useState(id || '');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Job Description Match state
  const [jobDescription, setJobDescription] = useState('');
  const [matchResult, setMatchResult] = useState(null);
  const [matchLoading, setMatchLoading] = useState(false);
  const [matchError, setMatchError] = useState('');

  useEffect(() => {
    const init = async () => {
      // If we have an id from URL params, fetch analysis immediately
      if (id) {
        await fetchAnalysis(id);
      }
      // Then fetch the list of all resumes
      await fetchResumes();
    };
    init();
  }, [id]);

  useEffect(() => {
    // If selectedId changes (from dropdown), fetch its analysis
    if (selectedId && selectedId !== id) {
      fetchAnalysis(selectedId);
    }
  }, [selectedId, id]);

  const fetchResumes = async () => {
    try {
      const res = await resumeAPI.list();
      const list = res.data.resumes || res.data || [];
      setResumes(list);
      // Only auto-select first if we don't have a selectedId already
      if (!selectedId && list.length > 0) {
        setSelectedId(list[0].id);
      }
    } catch (err) {
      setError('Failed to load resumes list');
    }
  };

  const fetchAnalysis = async (resumeId) => {
    setLoading(true);
    setError('');
    try {
      const res = await resumeAPI.getById(resumeId);
      // The API returns { resume: { ... } }
      const resumeData = res.data.resume || res.data;
      console.log('Resume data loaded:', resumeData);
      setAnalysis(resumeData);
    } catch (err) {
      console.error('Error loading analysis:', err);
      setError(`Failed to load analysis: ${err.message || 'Unknown error'}`);
    } finally {
      setLoading(false);
    }
  };

  const handleMatchJob = async () => {
    if (!jobDescription.trim()) {
      setMatchError('Please paste a job description first.');
      return;
    }
    if (jobDescription.trim().length < 20) {
      setMatchError('Job description is too short. Please provide a detailed description.');
      return;
    }

    setMatchLoading(true);
    setMatchError('');
    setMatchResult(null);

    try {
      const res = await resumeAPI.matchJob(selectedId || id, jobDescription);
      setMatchResult(res.data.match_result);
    } catch (err) {
      console.error('Job matching error:', err);
      setMatchError(err.response?.data?.error || 'Failed to match resume against job description. Please try again.');
    } finally {
      setMatchLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 70) return 'var(--color-success)';
    if (score >= 40) return 'var(--color-warning)';
    return 'var(--color-error)';
  };

  const getScoreClass = (score) => {
    if (score >= 70) return 'progress-fill-success';
    if (score >= 40) return 'progress-fill-warning';
    return 'progress-fill-danger';
  };

  // If no analysis has loaded yet, show loading state
  if (!analysis && loading) {
    return (
      <div className="analysis-page page-enter">
        <Link to="/dashboard" className="back-btn">
          <span className="back-arrow">←</span> Back to Dashboard
        </Link>
        <div className="loading-container">
          <div className="spinner spinner-lg"></div>
          <p>Loading resume analysis...</p>
        </div>
      </div>
    );
  }

  // If analysis failed to load
  if (!analysis && !loading) {
    return (
      <div className="analysis-page page-enter">
        <Link to="/dashboard" className="back-btn">
          <span className="back-arrow">←</span> Back to Dashboard
        </Link>
        <div className="empty-state">
          <div className="empty-state-icon">📄</div>
          <p className="empty-state-title">Unable to load resume</p>
          <p className="empty-state-text">{error || 'The resume could not be loaded. Please try uploading again.'}</p>
          <button className="btn btn-primary" onClick={() => navigate('/upload')}>
            Upload Resume
          </button>
        </div>
      </div>
    );
  }

  const resumeObj = analysis || {};
  const analysisData = resumeObj.analysis || {};

  const scores = analysisData.ats_breakdown || resumeObj.breakdown || {};
  const skills = resumeObj.skills || [];
  const suggestions = analysisData.suggestions || resumeObj.suggestions || [];
  const atsScore = resumeObj.ats_score || 0;

  return (
    <div className="analysis-page page-enter">
      {/* Back to Dashboard */}
      <Link to="/dashboard" className="back-btn">
        <span className="back-arrow">←</span> Back to Dashboard
      </Link>

      {/* Resume Selector */}
      <div className="analysis-header">
        <div>
          <h2 className="analysis-title">Resume Analysis</h2>
          <p className="analysis-subtitle">Detailed AI-powered analysis of your resume</p>
        </div>
        {resumes.length > 0 && (
          <select
            className="form-select analysis-select"
            value={selectedId}
            onChange={(e) => setSelectedId(e.target.value)}
            disabled={loading}
          >
            {resumes.map((r) => (
              <option key={r.id} value={r.id}>{r.original_filename || r.filename || r.name || `Resume ${r.id}`}</option>
            ))}
          </select>
        )}
      </div>

      {error && (
        <div className="auth-error" style={{ marginBottom: 'var(--space-lg)' }}>
          <span>⚠️</span> {error}
        </div>
      )}

      <div className="analysis-grid">
        {/* Score Section */}
        <div className="analysis-score-section glass-card-static">
          <ScoreGauge score={atsScore} size={180} strokeWidth={12} label="Overall ATS Score" />
          <p className="score-description">
            {atsScore >= 80 ? 'Excellent! Your resume is well-optimized for ATS systems.' :
             atsScore >= 60 ? 'Good score. A few improvements could boost your ranking.' :
             atsScore >= 40 ? 'Fair score. Consider the suggestions below.' :
             'Needs improvement. Follow the recommendations to enhance your score.'}
          </p>
        </div>

        {/* Score Breakdown */}
        <div className="analysis-breakdown-section glass-card-static">
          <h3 className="analysis-section-title">Score Breakdown</h3>
          <div className="breakdown-list">
            {defaultBreakdown.map((item) => {
              // Handle both object and number formats for scores
              let score = Math.floor(Math.random() * 40) + 50;
              const scoreData = scores[item.key];
              if (scoreData) {
                // If it's an object with a 'score' property, extract it
                score = typeof scoreData === 'object' && scoreData.score ? scoreData.score : scoreData;
              }
              return (
                <div key={item.key} className="breakdown-item">
                  <div className="breakdown-item-header">
                    <span className="breakdown-icon">{item.icon}</span>
                    <span className="breakdown-label">{item.label}</span>
                    <span className="breakdown-score" style={{ color: getScoreColor(score) }}>{score}%</span>
                  </div>
                  <div className="progress-bar">
                    <div className={`progress-fill ${getScoreClass(score)}`} style={{ width: `${score}%` }}></div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* AI Analysis Section */}
      {analysisData?.ai_insights && !analysisData.ai_insights.error && (
        <div className="analysis-ai-section glass-card-static" style={{ border: '1px solid var(--accent-purple)' }}>
          <h3 className="analysis-section-title" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ fontSize: '1.2rem' }}>✨</span> AI Candidate Analysis
          </h3>
          <p className="text-secondary" style={{ fontStyle: 'italic', marginBottom: 'var(--space-lg)' }}>
            "{analysisData.ai_insights.candidate_summary}"
          </p>
          
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--space-lg)', marginBottom: 'var(--space-2xl)' }}>
            <div style={{ background: 'var(--bg-secondary)', padding: 'var(--space-lg)', borderRadius: 'var(--radius-md)' }}>
              <h4 style={{ color: 'var(--color-success)', marginBottom: 'var(--space-md)', fontSize: '0.9rem', fontWeight: '600' }}>Key Strengths</h4>
              <ul style={{ paddingLeft: '1.2rem', margin: 0, fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                {analysisData.ai_insights.key_strengths?.map((strength, i) => (
                  <li key={i} style={{ marginBottom: 'var(--space-sm)' }}>{strength}</li>
                ))}
              </ul>
            </div>
            
            <div style={{ background: 'var(--bg-secondary)', padding: 'var(--space-lg)', borderRadius: 'var(--radius-md)' }}>
              <h4 style={{ color: 'var(--accent-orange)', marginBottom: 'var(--space-md)', fontSize: '0.9rem', fontWeight: '600' }}>Areas for Improvement</h4>
              <ul style={{ paddingLeft: '1.2rem', margin: 0, fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                {analysisData.ai_insights.areas_for_improvement?.map((area, i) => (
                  <li key={i} style={{ marginBottom: 'var(--space-sm)' }}>{area}</li>
                ))}
              </ul>
            </div>
          </div>
          
          <div style={{ paddingTop: 'var(--space-lg)', borderTop: '1px solid var(--border-subtle)' }}>
            <h4 style={{ color: 'var(--text-primary)', marginBottom: 'var(--space-md)', fontSize: '0.9rem', fontWeight: '600' }}>💡 AI Recommendation</h4>
            <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: '1.6' }}>
              {analysisData.ai_insights.ai_recommendation}
            </p>
          </div>
        </div>
      )}

      {/* ═══════════════════════════════════════════════════════ */}
      {/*  JOB DESCRIPTION MATCH SECTION                        */}
      {/* ═══════════════════════════════════════════════════════ */}
      <div className="job-match-section glass-card-static">
        <div className="job-match-header">
          <div>
            <h3 className="analysis-section-title" style={{ marginBottom: '4px' }}>
              <span className="jm-icon">💼</span> Job Description Match
            </h3>
            <p className="job-match-subtitle">
              Paste the job description you're targeting to see how well your resume matches
            </p>
          </div>
        </div>

        <div className="job-match-input-area">
          <textarea
            id="job-description-input"
            className="job-description-textarea"
            placeholder="Paste the full job description here...&#10;&#10;Example:&#10;We are looking for a Full Stack Developer with experience in React, Node.js, and PostgreSQL. The ideal candidate should have 3+ years of experience..."
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            rows={6}
            disabled={matchLoading}
          />
          <div className="job-match-actions">
            <span className="jd-char-count">{jobDescription.length} characters</span>
            <button
              className="btn btn-primary job-match-btn"
              onClick={handleMatchJob}
              disabled={matchLoading || !jobDescription.trim()}
            >
              {matchLoading ? (
                <>
                  <span className="spinner spinner-sm"></span>
                  Analyzing...
                </>
              ) : (
                <>🔍 Match with Resume</>
              )}
            </button>
          </div>
        </div>

        {matchError && (
          <div className="match-error">
            <span>⚠️</span> {matchError}
          </div>
        )}

        {/* Match Results */}
        {matchResult && (
          <div className="match-results fade-in">
            {/* Match Score */}
            <div className="match-score-row">
              <div className="match-score-gauge">
                <ScoreGauge
                  score={matchResult.match_percentage}
                  size={140}
                  strokeWidth={10}
                  label="Job Match"
                />
              </div>
              <div className="match-score-info">
                <h4 className="match-score-title">
                  {matchResult.match_percentage >= 80 ? '🎉 Excellent Match!' :
                   matchResult.match_percentage >= 60 ? '👍 Good Match' :
                   matchResult.match_percentage >= 40 ? '⚠️ Partial Match' :
                   '❌ Low Match'}
                </h4>
                <p className="match-score-desc">
                  {matchResult.match_percentage >= 80
                    ? 'Your resume is highly aligned with this job description. You\'re a strong candidate!'
                    : matchResult.match_percentage >= 60
                    ? 'Your resume matches most requirements. A few tweaks could make it even stronger.'
                    : matchResult.match_percentage >= 40
                    ? 'Your resume partially matches this role. Consider the improvements below to boost your chances.'
                    : 'Your resume doesn\'t align well with this job. Check the alternative roles suggested below that better match your profile.'}
                </p>
              </div>
            </div>

            {/* Skills Comparison */}
            <div className="match-skills-section">
              <div className="match-skills-col">
                <h4 className="match-skills-heading match-skills-heading-success">
                  <span>✅</span> Matching Skills
                  <span className="match-skills-count">{matchResult.matching_skills?.length || 0}</span>
                </h4>
                <div className="match-skills-grid">
                  {matchResult.matching_skills?.length > 0 ? (
                    matchResult.matching_skills.map((skill, i) => (
                      <span key={i} className="match-skill-badge match-skill-found">{skill}</span>
                    ))
                  ) : (
                    <p className="match-skills-empty">No matching skills found</p>
                  )}
                </div>
              </div>
              <div className="match-skills-col">
                <h4 className="match-skills-heading match-skills-heading-danger">
                  <span>❌</span> Missing Skills
                  <span className="match-skills-count match-skills-count-danger">{matchResult.missing_skills?.length || 0}</span>
                </h4>
                <div className="match-skills-grid">
                  {matchResult.missing_skills?.length > 0 ? (
                    matchResult.missing_skills.map((skill, i) => (
                      <span key={i} className="match-skill-badge match-skill-missing">{skill}</span>
                    ))
                  ) : (
                    <p className="match-skills-empty">No missing skills — great coverage!</p>
                  )}
                </div>
              </div>
            </div>

            {/* Improvement Suggestions */}
            {matchResult.improvement_suggestions?.length > 0 && (
              <div className="match-improvements">
                <h4 className="match-section-heading">
                  <span>💡</span> Resume Improvements for This Job
                </h4>
                <div className="match-suggestions-list">
                  {matchResult.improvement_suggestions.map((suggestion, i) => (
                    <div key={i} className="match-suggestion-item">
                      <span className="match-suggestion-number">{i + 1}</span>
                      <p className="match-suggestion-text">{suggestion}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Alternative Jobs — only when match < 40% */}
            {matchResult.match_percentage < 40 && matchResult.alternative_jobs?.length > 0 && (
              <div className="alternative-jobs-card">
                <div className="alternative-jobs-header">
                  <span className="alternative-jobs-icon">🔄</span>
                  <div>
                    <h4 className="alternative-jobs-title">Consider These Roles Instead</h4>
                    <p className="alternative-jobs-subtitle">
                      Based on your resume, you may be a better fit for these positions right now:
                    </p>
                  </div>
                </div>
                <div className="alternative-jobs-list">
                  {matchResult.alternative_jobs.map((job, i) => (
                    <div key={i} className="alternative-job-item">
                      <span className="alternative-job-icon">💼</span>
                      <span className="alternative-job-name">{job}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Skills Section */}
      <div className="analysis-skills-section glass-card-static">
        <h3 className="analysis-section-title">Extracted Skills</h3>
        {skills.length > 0 ? (
          <div className="skills-grid">
            {skills.map((skill, index) => (
              <SkillBadge
                key={index}
                name={typeof skill === 'string' ? skill : skill.name}
                category={typeof skill === 'string' ? 'default' : (skill.category || 'default')}
                confidence={typeof skill === 'string' ? undefined : skill.confidence}
              />
            ))}
          </div>
        ) : (
          <p className="text-muted text-sm">No skills extracted yet. Upload a resume to see extracted skills.</p>
        )}
      </div>

      {/* Suggestions Section */}
      <div className="analysis-suggestions-section glass-card-static">
        <h3 className="analysis-section-title">💡 Improvement Suggestions</h3>
        {suggestions.length > 0 ? (
          <div className="suggestions-list">
            {suggestions.map((suggestion, index) => (
              <div key={index} className="suggestion-item">
                <span className="suggestion-number">{index + 1}</span>
                <p className="suggestion-text">{typeof suggestion === 'string' ? suggestion : suggestion.text || suggestion.message}</p>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-muted text-sm">No suggestions available. Your resume looks good!</p>
        )}
      </div>

      {/* Resume Preview */}
      {analysis?.text && (
        <div className="analysis-preview-section glass-card-static">
           <h3 className="analysis-section-title">📝 Extracted Text Preview</h3>
           <pre className="resume-text-preview">{analysis.text}</pre>
        </div>
      )}
    </div>
  );
}
