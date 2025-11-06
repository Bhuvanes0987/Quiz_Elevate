
from flask import Blueprint, request, jsonify
from ..models import Question, Test, TestQuestion
from ..db import db

bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@bp.route('/questions', methods=['POST'])
def create_question():
    data = request.json or {}
    q = Question(subject=data.get('subject'), chapter=data.get('chapter'), qtype=data.get('qtype'),
                 content=data.get('content'), choices=data.get('choices'), correct_answer=data.get('correct_answer'))
    db.session.add(q); db.session.commit()
    return jsonify({'ok': True, 'id': q.id})

@bp.route('/tests', methods=['POST'])
def create_test():
    data = request.json or {}
    t = Test(name=data.get('name'), class_grade=data.get('class_grade'), duration_seconds=data.get('duration_seconds',900))
    db.session.add(t); db.session.commit()
    qids = data.get('question_ids', [])
    pos = 0
    for qid in qids:
        tq = TestQuestion(test_id=t.id, question_id=qid, position=pos)
        db.session.add(tq); pos += 1
    db.session.commit()
    return jsonify({'ok': True, 'test_id': t.id})
