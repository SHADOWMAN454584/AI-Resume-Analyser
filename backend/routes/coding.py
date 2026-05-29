"""
Coding challenge routes – problems listing, code execution, submission.
"""
import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from models.interview import CodingTest
from services.code_executor import get_all_problems, get_problem, execute_code

coding_bp = Blueprint('coding', __name__, url_prefix='/api/coding')


@coding_bp.route('/problems', methods=['GET'])
def list_problems():
    """
    Return all coding problems.
    Expected outputs are hidden from the client.
    """
    problems = get_all_problems(include_expected=False)
    return jsonify({
        'problems': problems,
        'count': len(problems)
    }), 200


@coding_bp.route('/run', methods=['POST'])
@jwt_required()
def run_code():
    """
    Run code against the first 2 test cases (for quick testing).
    Expects JSON: { problem_id: str, language: str, code: str }
    """
    user_id = int(get_jwt_identity())
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body is required'}), 400

    problem_id = data.get('problem_id', '')
    language = data.get('language', '').lower()
    code = data.get('code', '')

    # Validation
    if not problem_id:
        return jsonify({'error': 'problem_id is required'}), 400
    if not language:
        return jsonify({'error': 'language is required'}), 400
    if language not in ('python', 'javascript'):
        return jsonify({'error': 'Supported languages: python, javascript'}), 400
    if not code or not code.strip():
        return jsonify({'error': 'code is required'}), 400

    problem = get_problem(problem_id)
    if not problem:
        return jsonify({'error': f'Problem "{problem_id}" not found'}), 404

    # Run against first 2 test cases only
    test_cases = problem['test_cases'][:2]
    time_limit = problem.get('time_limit', 10)

    try:
        result = execute_code(code, language, test_cases, time_limit)
        return jsonify({
            'message': 'Code executed (quick run)',
            'problem_id': problem_id,
            'language': language,
            'result': result
        }), 200
    except Exception as e:
        return jsonify({'error': f'Execution failed: {str(e)}'}), 500


@coding_bp.route('/submit', methods=['POST'])
@jwt_required()
def submit_code():
    """
    Submit code to run against ALL test cases and save result to DB.
    Expects JSON: { problem_id: str, language: str, code: str }
    """
    user_id = int(get_jwt_identity())
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body is required'}), 400

    problem_id = data.get('problem_id', '')
    language = data.get('language', '').lower()
    code = data.get('code', '')

    # Validation
    if not problem_id:
        return jsonify({'error': 'problem_id is required'}), 400
    if not language:
        return jsonify({'error': 'language is required'}), 400
    if language not in ('python', 'javascript'):
        return jsonify({'error': 'Supported languages: python, javascript'}), 400
    if not code or not code.strip():
        return jsonify({'error': 'code is required'}), 400

    problem = get_problem(problem_id)
    if not problem:
        return jsonify({'error': f'Problem "{problem_id}" not found'}), 404

    # Run against ALL test cases
    test_cases = problem['test_cases']
    time_limit = problem.get('time_limit', 10)

    try:
        result = execute_code(code, language, test_cases, time_limit)

        # Save to database
        coding_test = CodingTest(
            user_id=user_id,
            problem_id=problem_id,
            problem_title=problem['title'],
            language=language,
            code=code,
            passed=(result['passed'] == result['total']),
            execution_time=result.get('execution_time', 0)
        )
        coding_test.set_result(result)
        db.session.add(coding_test)
        db.session.commit()

        return jsonify({
            'message': 'Code submitted and evaluated',
            'submission_id': coding_test.id,
            'problem_id': problem_id,
            'problem_title': problem['title'],
            'language': language,
            'result': result,
            'all_passed': result['passed'] == result['total']
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Submission failed: {str(e)}'}), 500


@coding_bp.route('/results', methods=['GET'])
@jwt_required()
def coding_results():
    """Return the current user's past coding test results."""
    user_id = int(get_jwt_identity())
    tests = CodingTest.query.filter_by(user_id=user_id).order_by(
        CodingTest.created_at.desc()
    ).all()

    return jsonify({
        'results': [t.to_dict() for t in tests],
        'count': len(tests)
    }), 200
