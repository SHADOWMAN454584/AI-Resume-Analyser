import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Area, AreaChart } from 'recharts';
import { dashboardAPI } from '../api/api';
import StatsCard from '../components/StatsCard';
import './Dashboard.css';

const CHART_COLORS = ['#06b6d4', '#3b82f6', '#8b5cf6', '#10b981', '#f59e0b', '#ef4444', '#ec4899', '#6366f1'];

const defaultStats = {
  total_resumes: 0,
  avg_ats_score: 0,
  interviews_done: 0,
  coding_tests: 0,
};

const defaultProgress = [
  { date: 'Week 1', score: 45 },
  { date: 'Week 2', score: 52 },
  { date: 'Week 3', score: 58 },
  { date: 'Week 4', score: 65 },
  { date: 'Week 5', score: 72 },
  { date: 'Week 6', score: 78 },
];

const defaultSkills = [
  { name: 'Python', value: 30 },
  { name: 'JavaScript', value: 25 },
  { name: 'React', value: 20 },
  { name: 'SQL', value: 15 },
  { name: 'AWS', value: 10 },
];

const recentActivity = [
  { icon: '📄', text: 'Resume uploaded and analyzed', time: '2 min ago', color: 'var(--accent-cyan)' },
  { icon: '🎤', text: 'Completed mock interview (85/100)', time: '1 hour ago', color: 'var(--accent-purple)' },
  { icon: '💻', text: 'Solved "Two Sum" coding problem', time: '3 hours ago', color: 'var(--color-success)' },
  { icon: '📊', text: 'ATS score improved to 78%', time: 'Yesterday', color: 'var(--accent-blue)' },
];

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="chart-tooltip">
        <p className="chart-tooltip-label">{label}</p>
        <p className="chart-tooltip-value">{payload[0].value}%</p>
      </div>
    );
  }
  return null;
};

export default function Dashboard() {
  const [stats, setStats] = useState(defaultStats);
  const [skills, setSkills] = useState(defaultSkills);
  const [progress, setProgress] = useState(defaultProgress);
  const [latestResume, setLatestResume] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const [statsRes, skillsRes, progressRes, latestRes] = await Promise.allSettled([
          dashboardAPI.getStats(),
          dashboardAPI.getSkills(),
          dashboardAPI.getProgress(),
          dashboardAPI.getLatestResume()
        ]);

        if (statsRes.status === 'fulfilled') {
          const statsData = statsRes.value.data?.stats || statsRes.value.data || defaultStats;
          // Map backend naming to frontend naming
          setStats({
            total_resumes: statsData.total_resumes,
            avg_ats_score: statsData.avg_ats_score,
            interviews_done: statsData.total_interviews,
            coding_tests: statsData.total_coding_tests,
          });
        }
        
        if (skillsRes.status === 'fulfilled') {
          const backendSkills = skillsRes.value.data?.skills;
          if (backendSkills && backendSkills.length > 0) {
            setSkills(backendSkills.map(s => ({ name: s.skill, value: s.count })));
          }
        }
        
        if (progressRes.status === 'fulfilled') {
          const atsProgress = progressRes.value.data?.ats_progress;
          if (atsProgress && atsProgress.length > 0) {
            // Map the progress to have a valid date and score
            setProgress(atsProgress.map((p, index) => ({ 
              date: new Date(p.date).toLocaleDateString(undefined, {month: 'short', day: 'numeric'}), 
              score: p.score 
            })));
          }
        }

        if (latestRes.status === 'fulfilled') {
          setLatestResume(latestRes.value.data?.latest_resume);
        }
      } catch (err) {
        console.error('Dashboard fetch error:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  return (
    <div className="dashboard-page page-enter">
      {/* Stats Row */}
      <div className="dashboard-stats-grid">
        <StatsCard icon="📄" label="Total Resumes" value={stats.total_resumes || 0} trend="up" trendValue="+3" />
        <StatsCard icon="🎯" label="Avg ATS Score" value={stats.avg_ats_score || 0} suffix="%" trend="up" trendValue="+5%" />
        <StatsCard icon="🎤" label="Interviews Done" value={stats.interviews_done || 0} trend="up" trendValue="+2" />
        <StatsCard icon="💻" label="Coding Tests" value={stats.coding_tests || 0} trend="up" trendValue="+1" />
      </div>

      {/* Charts Row */}
      <div className="dashboard-charts-grid">
        {/* ATS Score Trend */}
        <div className="dashboard-chart-card glass-card-static">
          <div className="chart-card-header">
            <h3 className="chart-title">ATS Score Trend</h3>
            <span className="badge badge-primary">Last 6 weeks</span>
          </div>
          <div className="chart-container">
            {loading ? (
              <div className="loading-container"><div className="spinner"></div></div>
            ) : (
              <ResponsiveContainer width="100%" height={280}>
                <AreaChart data={progress}>
                  <defs>
                    <linearGradient id="scoreGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#06b6d4" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                  <XAxis dataKey="date" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                  <YAxis stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} domain={[0, 100]} />
                  <Tooltip content={<CustomTooltip />} />
                  <Area type="monotone" dataKey="score" stroke="#06b6d4" strokeWidth={3} fill="url(#scoreGradient)" dot={{ fill: '#06b6d4', r: 5, strokeWidth: 2, stroke: '#0a0e1a' }} activeDot={{ r: 7, stroke: '#06b6d4', strokeWidth: 2, fill: '#0a0e1a' }} />
                </AreaChart>
              </ResponsiveContainer>
            )}
          </div>
        </div>

        {/* Skill Distribution */}
        <div className="dashboard-chart-card glass-card-static">
          <div className="chart-card-header">
            <h3 className="chart-title">Skill Distribution</h3>
            <span className="badge badge-purple">Top skills</span>
          </div>
          <div className="chart-container">
            {loading ? (
              <div className="loading-container"><div className="spinner"></div></div>
            ) : (
              <ResponsiveContainer width="100%" height={280}>
                <PieChart>
                  <Pie
                    data={skills}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    paddingAngle={4}
                    dataKey="value"
                    stroke="none"
                  >
                    {skills.map((_, index) => (
                      <Cell key={index} fill={CHART_COLORS[index % CHART_COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      background: 'var(--bg-secondary)',
                      border: '1px solid var(--border-subtle)',
                      borderRadius: 'var(--radius-md)',
                      color: 'var(--text-primary)',
                      fontSize: '13px',
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            )}
          </div>
          <div className="chart-legend">
            {skills.map((skill, index) => (
              <div key={skill.name} className="legend-item">
                <span className="legend-dot" style={{ background: CHART_COLORS[index % CHART_COLORS.length] }}></span>
                <span className="legend-label">{skill.name}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Bottom Row */}
      <div className="dashboard-bottom-grid">
        {/* Latest Resume Insights */}
        <div className="dashboard-activity-card glass-card-static" style={{ display: 'flex', flexDirection: 'column' }}>
          <h3 className="card-section-title">Latest Resume Insights</h3>
          {loading ? (
             <div className="loading-container"><div className="spinner"></div></div>
          ) : latestResume ? (
            <div className="activity-timeline" style={{ flex: 1, overflowY: 'auto', gap: '1rem' }}>
              <div className="activity-item">
                <div className="activity-icon-wrapper" style={{ borderColor: 'var(--accent-cyan)' }}>
                  <span className="activity-icon">📄</span>
                </div>
                <div className="activity-content">
                  <p className="activity-text" style={{ fontWeight: 600 }}>File: {latestResume.original_filename}</p>
                  <span className="activity-time">ATS Score: {latestResume.ats_score}%</span>
                </div>
              </div>
              
              {latestResume.analysis?.entities?.emails?.length > 0 && (
                <div className="activity-item">
                  <div className="activity-icon-wrapper" style={{ borderColor: 'var(--accent-purple)' }}>
                    <span className="activity-icon">📧</span>
                  </div>
                  <div className="activity-content">
                    <p className="activity-text">Contact info extracted</p>
                    <span className="activity-time">{latestResume.analysis.entities.emails.join(', ')}</span>
                  </div>
                </div>
              )}
              
              {latestResume.analysis?.skills_count > 0 || (latestResume.skills && latestResume.skills.length > 0) ? (
                <div className="activity-item">
                  <div className="activity-icon-wrapper" style={{ borderColor: 'var(--accent-blue)' }}>
                    <span className="activity-icon">🛠️</span>
                  </div>
                  <div className="activity-content">
                    <p className="activity-text">Technical Skills</p>
                    <span className="activity-time">{latestResume.skills.slice(0, 5).map(s => s.skill).join(', ')} {...(latestResume.skills.length > 5 ? ['and more'] : [])}</span>
                  </div>
                </div>
              ) : null}

              {latestResume.analysis?.ai_insights && !latestResume.analysis.ai_insights.error && (
                <div className="activity-item">
                  <div className="activity-icon-wrapper" style={{ borderColor: 'var(--accent-orange)' }}>
                    <span className="activity-icon">✨</span>
                  </div>
                  <div className="activity-content">
                    <p className="activity-text">AI Summary</p>
                    <span className="activity-time">{latestResume.analysis.ai_insights.candidate_summary}</span>
                  </div>
                </div>
              )}

              {latestResume.analysis?.experience_years != null && (
                <div className="activity-item">
                  <div className="activity-icon-wrapper" style={{ borderColor: 'var(--color-success)' }}>
                    <span className="activity-icon">💼</span>
                  </div>
                  <div className="activity-content">
                    <p className="activity-text">Experience Extracted</p>
                    <span className="activity-time">{latestResume.analysis.experience_years} years estimated</span>
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-muted)' }}>
              No recent resume found. Upload one to see insights.
            </div>
          )}
        </div>

        {/* Quick Actions */}
        <div className="dashboard-actions-card glass-card-static">
          <h3 className="card-section-title">Quick Actions</h3>
          <div className="quick-actions-grid">
            <Link to="/upload" className="quick-action-btn">
              <span className="qa-icon">📤</span>
              <span className="qa-label">Upload Resume</span>
              <span className="qa-desc">Analyze a new resume</span>
            </Link>
            <Link to="/interview" className="quick-action-btn">
              <span className="qa-icon">🎤</span>
              <span className="qa-label">Start Interview</span>
              <span className="qa-desc">Practice AI mock interview</span>
            </Link>
            <Link to="/coding" className="quick-action-btn">
              <span className="qa-icon">💻</span>
              <span className="qa-label">Coding Test</span>
              <span className="qa-desc">Solve coding challenges</span>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
