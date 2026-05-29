"""
Interview routes – question generation, answer submission, history.
"""
import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from models.resume import Resume
from models.interview import InterviewSession
from services.nlp_engine import extract_experience_years
from services.question_generator import generate_questions, evaluate_answer

interview_bp = Blueprint('interview', __name__, url_prefix='/api/interview')


@interview_bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_interview():
    """
    Generate interview questions based on a resume's extracted skills.
    Expects JSON: { resume_id: int, job_role?: string }
    """
    user_id = int(get_jwt_identity())
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body is required'}), 400

    resume_id = data.get('resume_id')
    job_role = data.get('job_role')

    if not resume_id:
        return jsonify({'error': 'resume_id is required'}), 400

    # Fetch the resume
    resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
    if not resume:
        return jsonify({'error': 'Resume not found'}), 404

    # Extract skills and experience from the stored resume
    skills = resume.get_skills()
    analysis = resume.get_analysis()
    experience_years = analysis.get('experience_years', 0)

    # If experience wasn't stored, re-calculate
    if not experience_years and resume.raw_text:
        experience_years = extract_experience_years(resume.raw_text)

    # Generate questions
    try:
        questions = generate_questions(skills, experience_years, job_role)

        # Strip keywords and sample_answer from the response to the client
        client_questions = []
        for q in questions:
            client_questions.append({
                'id': q['id'],
                'text': q['text'],
                'category': q['category'],
                'difficulty': q['difficulty'],
                'skill_related': q['skill_related']
            })

        # Create interview session
        session = InterviewSession(
            user_id=user_id,
            resume_id=resume_id
        )
        session.set_questions(questions)  # Store full questions with answers for evaluation
        db.session.add(session)
        db.session.commit()

        return jsonify({
            'message': 'Interview questions generated',
            'session_id': session.id,
            'questions': client_questions,
            'total_questions': len(client_questions)
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to generate questions: {str(e)}'}), 500


@interview_bp.route('/submit', methods=['POST'])
@jwt_required()
def submit_answers():
    """
    Submit answers for an interview session and get evaluated results.
    Expects JSON: { session_id: int, answers: { "question_id": "answer_text", ... } }
    """
    user_id = int(get_jwt_identity())
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body is required'}), 400

    session_id = data.get('session_id')
    answers = data.get('answers', {})

    if not session_id:
        return jsonify({'error': 'session_id is required'}), 400
    if not answers:
        return jsonify({'error': 'answers object is required'}), 400

    # Fetch session
    session = InterviewSession.query.filter_by(id=session_id, user_id=user_id).first()
    if not session:
        return jsonify({'error': 'Interview session not found'}), 404

    questions = session.get_questions()
    if not questions:
        return jsonify({'error': 'No questions found for this session'}), 400

    # Evaluate each answer
    try:
        evaluations = []
        total_score = 0.0
        answered_count = 0

        for q in questions:
            q_id = str(q['id'])
            answer_text = answers.get(q_id, '')

            if answer_text:
                result = evaluate_answer(q, answer_text)
                answered_count += 1
            else:
                result = {
                    'score': 0,
                    'feedback': 'No answer provided.'
                }

            total_score += result['score']
            evaluations.append({
                'question_id': q['id'],
                'question_text': q['text'],
                'category': q['category'],
                'your_answer': answer_text,
                'score': result['score'],
                'max_score': 10,
                'feedback': result['feedback'],
                'sample_answer': q.get('sample_answer', '')
            })

        # Calculate overall score as percentage
        max_possible = len(questions) * 10
        overall_score = round((total_score / max_possible) * 100, 1) if max_possible > 0 else 0

        feedback_summary = {
            'overall_score': overall_score,
            'total_questions': len(questions),
            'answered': answered_count,
            'total_points': round(total_score, 1),
            'max_points': max_possible,
            'evaluations': evaluations
        }

        # Update session
        session.set_answers(answers)
        session.score = overall_score
        session.set_feedback(feedback_summary)
        db.session.commit()

        return jsonify({
            'message': 'Answers evaluated successfully',
            'results': feedback_summary
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Evaluation failed: {str(e)}'}), 500


@interview_bp.route('/history', methods=['GET'])
@jwt_required()
def interview_history():
    """Return the current user's past interview sessions."""
    user_id = int(get_jwt_identity())
    sessions = InterviewSession.query.filter_by(user_id=user_id).order_by(
        InterviewSession.created_at.desc()
    ).all()

    results = []
    for s in sessions:
        session_data = s.to_dict()
        # Don't include full questions/answers/feedback in listing to keep response small
        session_data['question_count'] = len(s.get_questions())
        # Remove heavy fields from listing
        session_data.pop('questions', None)
        session_data.pop('answers', None)
        results.append(session_data)

    return jsonify({
        'sessions': results,
        'count': len(results)
    }), 200
