import { useState } from 'react';
import './QuestionCard.css';

export default function QuestionCard({
  index,
  question,
  category,
  difficulty,
  answer,
  onAnswerChange,
  score,
  feedback,
  submitted,
}) {
  const [expanded, setExpanded] = useState(!submitted);

  const difficultyClass = {
    easy: 'badge-success',
    medium: 'badge-warning',
    hard: 'badge-danger',
  }[difficulty?.toLowerCase()] || 'badge-primary';

  const categoryIcons = {
    technical: '⚙️',
    behavioral: '🧠',
    situational: '🎯',
    coding: '💻',
    system_design: '🏗️',
  };

  return (
    <div className={`question-card glass-card ${submitted ? 'question-card-submitted' : ''}`}>
      <div className="question-card-header" onClick={() => setExpanded(!expanded)}>
        <div className="question-card-number">Q{index + 1}</div>
        <div className="question-card-meta">
          <h3 className="question-card-text">{question}</h3>
          <div className="question-card-tags">
            {category && (
              <span className="badge badge-primary">
                {categoryIcons[category?.toLowerCase()] || '📝'} {category}
              </span>
            )}
            {difficulty && (
              <span className={`badge ${difficultyClass}`}>
                {difficulty}
              </span>
            )}
          </div>
        </div>
        <div className="question-card-toggle">
          {submitted && score !== undefined && (
            <div className="question-score" style={{
              color: score >= 7 ? 'var(--color-success)' : score >= 4 ? 'var(--color-warning)' : 'var(--color-error)'
            }}>
              {score}/10
            </div>
          )}
          <span className="toggle-icon">{expanded ? '▲' : '▼'}</span>
        </div>
      </div>

      {expanded && (
        <div className="question-card-body">
          {!submitted ? (
            <textarea
              className="form-input question-answer-input"
              placeholder="Type your answer here..."
              value={answer || ''}
              onChange={(e) => onAnswerChange && onAnswerChange(e.target.value)}
              rows={5}
            />
          ) : (
            <div className="question-result">
              <div className="answer-section">
                <h4 className="answer-label">Your Answer:</h4>
                <p className="answer-text">{answer || 'No answer provided'}</p>
              </div>
              {feedback && (
                <div className="feedback-section">
                  <h4 className="feedback-label">💡 Feedback:</h4>
                  <p className="feedback-text">{feedback}</p>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
