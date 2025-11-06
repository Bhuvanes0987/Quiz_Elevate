
import random
from datetime import datetime, timedelta
from ..models import OTP
from ..db import db

def create_otp(destination, ttl_minutes=10):
    code = f"{random.randint(100000,999999)}"
    expires_at = datetime.utcnow() + timedelta(minutes=ttl_minutes)
    otp = OTP(phone_or_email=destination, code=code, expires_at=expires_at)
    db.session.add(otp)
    db.session.commit()
    print(f'[OTP] Send to {destination}: {code}')
    return otp

def verify_otp(destination, code):
    otp = OTP.query.filter_by(phone_or_email=destination, code=code, used=False).order_by(OTP.created_at.desc()).first()
    if not otp:
        return False, 'not_found'
    if otp.expires_at < datetime.utcnow():
        return False, 'expired'
    otp.used = True
    db.session.commit()
    return True, None
