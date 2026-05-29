"""
Resume routes – upload, analysis, listing, deletion.
"""
import os
import json
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from models.resume import Resume
from services.pdf_parser import parse_pdf, extract_sections
from services.nlp_engine import extract_skills, extract_entities, extract_experience_years
from services.ats_scorer import calculate_ats_score
from services.ai_analyzer import analyze_resume_with_ai
from utils.helpers import allowed_file, generate_unique_filename

resume_bp = Blueprint('resume', __name__, url_prefix='/api/resume')


@resume_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_resume():
    """
    Upload a PDF resume, parse it, extract skills, calculate ATS score,
    and save the full analysis to the database.
    """
    user_id = int(get_jwt_identity())

    # --- File validation ---
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided. Send a PDF file with key "file".'}), 400

    file = request.files['file']
    if file.filename == '' or not file.filename:
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Only PDF files are allowed'}), 400

    # --- Save file ---
    try:
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)

        original_filename = file.filename
        unique_filename = generate_unique_filename(original_filename)
        file_path = os.path.join(upload_folder, unique_filename)
        file.save(file_path)
    except Exception as e:
        return jsonify({'error': f'Failed to save file: {str(e)}'}), 500

    # --- Parse PDF ---
    try:
        raw_text = parse_pdf(file_path)
    except ValueError as e:
        # Cleanup file on parse failure
        if os.path.exists(file_path):
            os.remove(file_path)
        return jsonify({'error': str(e)}), 422

    # --- Extract data ---
    try:
        sections = extract_sections(raw_text)
        skills = extract_skills(raw_text)
        entities = extract_entities(raw_text)
        experience_years = extract_experience_years(raw_text)
        ats_result = calculate_ats_score(raw_text, skills, sections)
        
        # --- Run AI Analysis using Groq ---
        ai_insights = analyze_resume_with_ai(raw_text)

        analysis = {
            'sections': sections,
            'entities': entities,
            'experience_years': experience_years,
            'ats_breakdown': ats_result['breakdown'],
            'suggestions': ats_result['suggestions'],
            'word_count': len(raw_text.split()),
            'skill_count': len(skills),
            'ai_insights': ai_insights
        }

        # --- Save to database ---
        resume = Resume(
            user_id=user_id,
            filename=unique_filename,
            original_filename=original_filename,
            raw_text=raw_text
        )
        resume.set_skills(skills)
        resume.ats_score = ats_result['overall_score']
        resume.set_analysis(analysis)

        db.session.add(resume)
        db.session.commit()

        return jsonify({
            'message': 'Resume uploaded and analyzed successfully',
            'resume': resume.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500


@resume_bp.route('/list', methods=['GET'])
@jwt_required()
def list_resumes():
    """Return all resumes for the current user."""
    user_id = int(get_jwt_identity())
    resumes = Resume.query.filter_by(user_id=user_id).order_by(Resume.uploaded_at.desc()).all()

    return jsonify({
        'resumes': [r.to_dict() for r in resumes],
        'count': len(resumes)
    }), 200


@resume_bp.route('/<int:resume_id>', methods=['GET'])
@jwt_required()
def get_resume(resume_id):
    """Return a single resume analysis by ID."""
    user_id = int(get_jwt_identity())
    resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()

    if not resume:
        return jsonify({'error': 'Resume not found'}), 404

    return jsonify({'resume': resume.to_dict()}), 200


@resume_bp.route('/<int:resume_id>', methods=['DELETE'])
@jwt_required()
def delete_resume(resume_id):
    """Delete a resume file and database record."""
    user_id = int(get_jwt_identity())
    resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()

    if not resume:
        return jsonify({'error': 'Resume not found'}), 404

    # Delete the physical file
    try:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], resume.filename)
        if os.path.exists(file_path):
            os.remove(file_path)
    except OSError:
        pass  # File may already be gone

    # Delete database record
    try:
        db.session.delete(resume)
        db.session.commit()
        return jsonify({'message': 'Resume deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete resume: {str(e)}'}), 500
