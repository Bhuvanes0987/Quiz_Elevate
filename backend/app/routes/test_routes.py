
from flask import Blueprint, request, jsonify
from ..models import Test, Question, TestQuestion, TestAttempt, QuestionAttempt
from ..db import db
from ..utils.ai_eval import evaluate_answers
from datetime import datetime

bp = Blueprint('tests', __name__, url_prefix='/api/tests')

@bp.route('/class/<int:grade>/', methods=['GET'])
def tests_by_class(grade):
    tests = Test.query.filter_by(class_grade=grade).all()
    out = [{'id': t.id, 'name': t.name, 'duration_seconds': t.duration_seconds} for t in tests]
    return jsonify(out)

@bp.route('/<int:test_id>/start', methods=['POST'])
def start_test(test_id):
    data = request.json or {}
    user_id = data.get('user_id')
    test = Test.query.get(test_id)
    if not test:
        return jsonify({'error':'not found'}), 404
    attempt = TestAttempt(user_id=user_id, test_id=test.id, started_at=datetime.utcnow())
    db.session.add(attempt); db.session.commit()
    tq = TestQuestion.query.filter_by(test_id=test.id).order_by(TestQuestion.position).all()
    qlist = []
    for t in tq:
        q = Question.query.get(t.question_id)
        qlist.append({'id': q.id, 'content': q.content, 'qtype': q.qtype, 'choices': q.choices, 'time_limit_seconds': q.time_limit_seconds})
    return jsonify({'attempt_id': attempt.id, 'questions': qlist})

@bp.route('/<int:attempt_id>/submit', methods=['POST'])
def submit_attempt(attempt_id):
    data = request.json or {}
    answers = data.get('answers', [])
    prepared = []
    for a in answers:
        q = Question.query.get(a.get('question_id'))
        prepared.append({'question_id': q.id, 'response': a.get('response'), 'qtype': q.qtype, 'correct_answer': q.correct_answer})
    results = evaluate_answers(prepared)
    total = 0; correct = 0
    for r in results:
        total += r.get('max_score',1)
        correct += r.get('score',0)
    score = (correct/total*100) if total>0 else 0
    attempt = TestAttempt.query.get(attempt_id)
    attempt.finished_at = datetime.utcnow()
    attempt.score = score
    attempt.ai_score = score
    attempt.status = 'finished'
    db.session.commit()
    return jsonify({'score': score, 'results': results})
