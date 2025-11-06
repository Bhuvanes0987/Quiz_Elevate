
from flask import Blueprint, jsonify
from ..db import db
from ..models import TestAttempt
from sqlalchemy import func

bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')

@bp.route('/summary', methods=['GET'])
def summary():
    attempts = db.session.query(TestAttempt).count()
    avg = db.session.query(func.avg(TestAttempt.score)).scalar() or 0
    return jsonify({'attempts_total': attempts, 'avg_score': float(avg)})
