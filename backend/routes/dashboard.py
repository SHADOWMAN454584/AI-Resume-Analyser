"""
Dashboard routes – aggregate statistics, skills data, progress tracking.
"""
import json
from collections import Counter
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.resume import Resume
from models.interview import InterviewSession, CodingTest

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')


@dashboard_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    """
    Return aggregate statistics for the current user:
    total_resumes, avg_ats_score, total_interviews, avg_interview_score,
    total_coding_tests, coding_pass_rate.
    """
    user_id = int(get_jwt_identity())

    # Resumes
    resumes = Resume.query.filter_by(user_id=user_id).all()
    total_resumes = len(resumes)
    avg_ats_score = 0.0
    if resumes:
        scores = [r.ats_score for r in resumes if r.ats_score is not None]
        avg_ats_score = round(sum(scores) / len(scores), 1) if scores else 0.0

    # Interview sessions
    sessions = InterviewSession.query.filter_by(user_id=user_id).all()
    total_interviews = len(sessions)
    avg_interview_score = 0.0
    if sessions:
        interview_scores = [s.score for s in sessions if s.score is not None]
        avg_interview_score = round(sum(interview_scores) / len(interview_scores), 1) if interview_scores else 0.0

    # Coding tests
    coding_tests = CodingTest.query.filter_by(user_id=user_id).all()
    total_coding_tests = len(coding_tests)
    coding_pass_rate = 0.0
    if coding_tests:
        passed_count = sum(1 for t in coding_tests if t.passed)
        coding_pass_rate = round((passed_count / total_coding_tests) * 100, 1)

    return jsonify({
        'stats': {
            'total_resumes': total_resumes,
            'avg_ats_score': avg_ats_score,
            'total_interviews': total_interviews,
            'avg_interview_score': avg_interview_score,
            'total_coding_tests': total_coding_tests,
            'coding_pass_rate': coding_pass_rate
        }
    }), 200


@dashboard_bp.route('/skills', methods=['GET'])
@jwt_required()
def get_skills_data():
    """
    Aggregate skills from all user's resumes and return frequency data
    suitable for charts and visualizations.
    """
    user_id = int(get_jwt_identity())
    resumes = Resume.query.filter_by(user_id=user_id).all()

    skill_counter = Counter()
    category_counter = Counter()
    all_skills_detail = []

    for resume in resumes:
        skills = resume.get_skills()
        for skill in skills:
            skill_name = skill.get('skill', '')
            category = skill.get('category', 'Other')
            if skill_name:
                skill_counter[skill_name] += 1
                category_counter[category] += 1

    # Build frequency data
    skill_frequency = [
        {'skill': skill, 'count': count}
        for skill, count in skill_counter.most_common(50)
    ]

    category_frequency = [
        {'category': cat, 'count': count}
        for cat, count in category_counter.most_common()
    ]

    return jsonify({
        'skills': skill_frequency,
        'categories': category_frequency,
        'total_unique_skills': len(skill_counter),
        'total_categories': len(category_counter)
    }), 200


@dashboard_bp.route('/progress', methods=['GET'])
@jwt_required()
def get_progress():
    """
    Return time-series data for ATS scores, interview scores, and coding results
    to show progress over time.
    """
    user_id = int(get_jwt_identity())

    # ATS scores over time
    resumes = Resume.query.filter_by(user_id=user_id).order_by(Resume.uploaded_at.asc()).all()
    ats_progress = [
        {
            'date': r.uploaded_at.isoformat() if r.uploaded_at else None,
            'score': r.ats_score,
            'filename': r.original_filename
        }
        for r in resumes
    ]

    # Interview scores over time
    sessions = InterviewSession.query.filter_by(user_id=user_id).order_by(
        InterviewSession.created_at.asc()
    ).all()
    interview_progress = [
        {
            'date': s.created_at.isoformat() if s.created_at else None,
            'score': s.score,
            'session_id': s.id
        }
        for s in sessions
    ]

    # Coding test results over time
    coding_tests = CodingTest.query.filter_by(user_id=user_id).order_by(
        CodingTest.created_at.asc()
    ).all()
    coding_progress = [
        {
            'date': t.created_at.isoformat() if t.created_at else None,
            'passed': t.passed,
            'problem_title': t.problem_title,
            'execution_time': t.execution_time,
            'problem_id': t.problem_id
        }
        for t in coding_tests
    ]

    return jsonify({
        'ats_progress': ats_progress,
        'interview_progress': interview_progress,
        'coding_progress': coding_progress
    }), 200

@dashboard_bp.route('/latest_resume', methods=['GET'])
@jwt_required()
def get_latest_resume():
    """
    Return the most recently uploaded resume with its extracted info (entities, skills, ats_score).
    """
    user_id = int(get_jwt_identity())
    latest_resume = Resume.query.filter_by(user_id=user_id).order_by(Resume.uploaded_at.desc()).first()
    
    if not latest_resume:
        return jsonify({'message': 'No resumes found', 'latest_resume': None}), 200
        
    return jsonify({'latest_resume': latest_resume.to_dict()}), 200

