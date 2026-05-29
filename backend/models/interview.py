"""
Interview and Coding Test models.
"""
import json
from datetime import datetime, timezone
from models import db


class InterviewSession(db.Model):
    """Mock interview session record."""

    __tablename__ = 'interview_sessions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=True, index=True)
    questions_json = db.Column(db.Text, nullable=True)
    answers_json = db.Column(db.Text, nullable=True)
    score = db.Column(db.Float, nullable=True, default=0.0)
    feedback_json = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def get_questions(self):
        """Parse and return questions from JSON."""
        if self.questions_json:
            try:
                return json.loads(self.questions_json)
            except (json.JSONDecodeError, TypeError):
                return []
        return []

    def set_questions(self, questions_list):
        """Store questions as JSON string."""
        self.questions_json = json.dumps(questions_list, ensure_ascii=False)

    def get_answers(self):
        """Parse and return answers from JSON."""
        if self.answers_json:
            try:
                return json.loads(self.answers_json)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}

    def set_answers(self, answers_dict):
        """Store answers as JSON string."""
        self.answers_json = json.dumps(answers_dict, ensure_ascii=False)

    def get_feedback(self):
        """Parse and return feedback from JSON."""
        if self.feedback_json:
            try:
                return json.loads(self.feedback_json)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}

    def set_feedback(self, feedback_dict):
        """Store feedback as JSON string."""
        self.feedback_json = json.dumps(feedback_dict, ensure_ascii=False)

    def to_dict(self):
        """Serialize interview session to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'resume_id': self.resume_id,
            'questions': self.get_questions(),
            'answers': self.get_answers(),
            'score': self.score,
            'feedback': self.get_feedback(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<InterviewSession {self.id}>'


class CodingTest(db.Model):
    """Coding test submission record."""

    __tablename__ = 'coding_tests'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    problem_id = db.Column(db.String(50), nullable=False)
    problem_title = db.Column(db.String(200), nullable=False)
    language = db.Column(db.String(20), nullable=False)
    code = db.Column(db.Text, nullable=False)
    result_json = db.Column(db.Text, nullable=True)
    passed = db.Column(db.Boolean, default=False)
    execution_time = db.Column(db.Float, nullable=True, default=0.0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def get_result(self):
        """Parse and return result from JSON."""
        if self.result_json:
            try:
                return json.loads(self.result_json)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}

    def set_result(self, result_dict):
        """Store result as JSON string."""
        self.result_json = json.dumps(result_dict, ensure_ascii=False)

    def to_dict(self):
        """Serialize coding test to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'problem_id': self.problem_id,
            'problem_title': self.problem_title,
            'language': self.language,
            'code': self.code,
            'result': self.get_result(),
            'passed': self.passed,
            'execution_time': self.execution_time,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<CodingTest {self.problem_title}>'
