import { useState, useEffect } from 'react';
import './ScoreGauge.css';

export default function ScoreGauge({ score = 0, size = 160, strokeWidth = 10, label = 'ATS Score' }) {
  const [animatedScore, setAnimatedScore] = useState(0);
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const center = size / 2;

  useEffect(() => {
    const timer = setTimeout(() => setAnimatedScore(score), 100);
    return () => clearTimeout(timer);
  }, [score]);

  const offset = circumference - (animatedScore / 100) * circumference;

  const getColor = () => {
    if (animatedScore < 40) return '#dc2626';
    if (animatedScore < 70) return '#d97706';
    return '#059669';
  };

  const getGrade = () => {
    if (score >= 90) return 'A+';
    if (score >= 80) return 'A';
    if (score >= 70) return 'B';
    if (score >= 60) return 'C';
    if (score >= 50) return 'D';
    return 'F';
  };

  return (
    <div className="score-gauge">
      <svg width={size} height={size} className="score-gauge-svg">
        {/* Background circle */}
        <circle
          cx={center}
          cy={center}
          r={radius}
          fill="none"
          stroke="rgba(0,0,0,0.06)"
          strokeWidth={strokeWidth}
        />
        {/* Glow filter */}
        <defs>
          <filter id={`glow-${score}`}>
            <feGaussianBlur stdDeviation="3" result="glow" />
            <feMerge>
              <feMergeNode in="glow" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>
        {/* Progress circle */}
        <circle
          cx={center}
          cy={center}
          r={radius}
          fill="none"
          stroke={getColor()}
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          transform={`rotate(-90 ${center} ${center})`}
          className="score-gauge-progress"
          filter={`url(#glow-${score})`}
          style={{ transition: 'stroke-dashoffset 1.5s ease, stroke 0.5s ease' }}
        />
      </svg>
      <div className="score-gauge-content">
        <span className="score-gauge-value" style={{ color: getColor() }}>{Math.round(animatedScore)}</span>
        <span className="score-gauge-grade" style={{ color: getColor() }}>{getGrade()}</span>
      </div>
      <p className="score-gauge-label">{label}</p>
    </div>
  );
}
