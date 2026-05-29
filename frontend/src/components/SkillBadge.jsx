import './SkillBadge.css';

const categoryColors = {
  'programming': { bg: '#eff6ff', color: '#2563eb', border: '#dbeafe' },
  'framework': { bg: '#f5f3ff', color: '#7c3aed', border: '#ede9fe' },
  'database': { bg: '#f0fdfa', color: '#0d9488', border: '#ccfbf1' },
  'tool': { bg: '#fffbeb', color: '#d97706', border: '#fef3c7' },
  'soft_skill': { bg: '#ecfdf5', color: '#059669', border: '#d1fae5' },
  'cloud': { bg: '#eef2ff', color: '#4f46e5', border: '#e0e7ff' },
  'design': { bg: '#fdf2f8', color: '#db2777', border: '#fce7f3' },
  'default': { bg: '#f8fafc', color: '#64748b', border: '#e2e8f0' },
};

export default function SkillBadge({ name, category = 'default', confidence, onClick }) {
  const colors = categoryColors[category] || categoryColors.default;

  return (
    <span
      className={`skill-badge ${onClick ? 'skill-badge-clickable' : ''}`}
      style={{
        background: colors.bg,
        color: colors.color,
        borderColor: colors.border,
      }}
      onClick={onClick}
      title={confidence ? `Confidence: ${confidence}%` : undefined}
    >
      <span className="skill-badge-name">{name}</span>
      {confidence !== undefined && (
        <span className="skill-badge-confidence" style={{ background: colors.color }}>
          {confidence}%
        </span>
      )}
    </span>
  );
}
