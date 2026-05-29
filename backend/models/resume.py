"""
Resume model for storing parsed resume data and analysis results.
"""
import json
from datetime import datetime, timezone
from models import db


class Resume(db.Model):
    """Resume upload and analysis record."""

    __tablename__ = 'resumes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    filename = db.Column(db.String(256), nullable=False)
    original_filename = db.Column(db.String(256), nullable=False)
    raw_text = db.Column(db.Text, nullable=True)
    skills_json = db.Column(db.Text, nullable=True)  # JSON string
    ats_score = db.Column(db.Float, nullable=True, default=0.0)
    analysis_json = db.Column(db.Text, nullable=True)  # JSON string
    uploaded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    interview_sessions = db.relationship('InterviewSession', backref='resume', lazy='dynamic')

    def get_skills(self):
        """Parse and return skills from JSON string."""
        if self.skills_json:
            try:
                return json.loads(self.skills_json)
            except (json.JSONDecodeError, TypeError):
                return []
        return []

    def set_skills(self, skills_list):
        """Store skills as JSON string."""
        self.skills_json = json.dumps(skills_list, ensure_ascii=False)

    def get_analysis(self):
        """Parse and return analysis from JSON string."""
        if self.analysis_json:
            try:
                return json.loads(self.analysis_json)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}

    def set_analysis(self, analysis_dict):
        """Store analysis as JSON string."""
        self.analysis_json = json.dumps(analysis_dict, ensure_ascii=False)

    def to_dict(self):
        """Serialize resume to dictionary with parsed JSON fields."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'raw_text': self.raw_text,
            'skills': self.get_skills(),
            'ats_score': self.ats_score,
            'analysis': self.get_analysis(),
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None
        }

    def __repr__(self):
        return f'<Resume {self.original_filename}>'
