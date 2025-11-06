
from flask import Blueprint, request, jsonify
from ..utils.otp_service import create_otp, verify_otp
from ..models import User
from ..db import db
from datetime import datetime

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/send-otp', methods=['POST'])
def send_otp():
    data = request.json or {}
    dest = data.get('phone_or_email')
    if not dest:
        return jsonify({'error':'phone_or_email required'}), 400
    otp = create_otp(dest)
    return jsonify({'ok': True, 'otp_id': otp.id})

@bp.route('/verify-otp', methods=['POST'])
def verify_otp_route():
    data = request.json or {}
    dest = data.get('phone_or_email'); code = data.get('code')
    if not dest or not code:
        return jsonify({'error':'phone_or_email and code required'}), 400
    ok, err = verify_otp(dest, code)
    if not ok:
        return jsonify({'error': err}), 400
    user = User.query.filter_by(email=dest).first()
    created = False
    if not user:
        user = User(email=dest, username=dest.split('@')[0], created_at=datetime.utcnow())
        db.session.add(user); db.session.commit()
        created = True
    return jsonify({'ok': True, 'user': {'id': user.id, 'email': user.email}, 'created': created})
