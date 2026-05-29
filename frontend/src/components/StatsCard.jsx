import { useState, useEffect, useRef } from 'react';
import './StatsCard.css';

export default function StatsCard({ icon, label, value, trend, trendValue, prefix = '', suffix = '' }) {
  const [displayValue, setDisplayValue] = useState(0);
  const cardRef = useRef(null);
  const animated = useRef(false);

  useEffect(() => {
    const numericValue = typeof value === 'number' ? value : parseFloat(value) || 0;
    if (animated.current) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !animated.current) {
          animated.current = true;
          let start = 0;
          const duration = 1500;
          const startTime = performance.now();

          const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
            start = Math.round(eased * numericValue);
            setDisplayValue(start);
            if (progress < 1) requestAnimationFrame(animate);
          };
          requestAnimationFrame(animate);
        }
      },
      { threshold: 0.3 }
    );

    if (cardRef.current) observer.observe(cardRef.current);
    return () => observer.disconnect();
  }, [value]);

  const trendColor = trend === 'up' ? 'var(--color-success)' : trend === 'down' ? 'var(--color-error)' : 'var(--text-muted)';
  const trendIcon = trend === 'up' ? '↑' : trend === 'down' ? '↓' : '';

  return (
    <div className="stats-card glass-card" ref={cardRef}>
      <div className="stats-card-header">
        <span className="stats-card-icon">{icon}</span>
        {trend && (
          <span className="stats-card-trend" style={{ color: trendColor }}>
            {trendIcon} {trendValue}
          </span>
        )}
      </div>
      <div className="stats-card-value">
        {prefix}{displayValue}{suffix}
      </div>
      <div className="stats-card-label">{label}</div>
    </div>
  );
}
