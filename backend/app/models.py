
from datetime import datetime
from .db import db
from sqlalchemy.dialects.mysql import JSON

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(150))
    password_hash = db.Column(db.String(255))
    class_grade = db.Column(db.SmallInteger)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class OTP(db.Model):
    __tablename__ = 'otp_codes'
    id = db.Column(db.Integer, primary_key=True)
    phone_or_email = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(16), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100))
    chapter = db.Column(db.String(255))
    qtype = db.Column(db.String(20))  # mcq, fill, match
    content = db.Column(db.Text)
    choices = db.Column(JSON, nullable=True)
    correct_answer = db.Column(JSON, nullable=True)
    time_limit_seconds = db.Column(db.Integer, default=60)
    difficulty = db.Column(db.SmallInteger, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Test(db.Model):
    __tablename__ = 'tests'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    class_grade = db.Column(db.SmallInteger)
    duration_seconds = db.Column(db.Integer, default=900)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TestQuestion(db.Model):
    __tablename__ = 'test_questions'
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    position = db.Column(db.Integer, default=0)

class TestAttempt(db.Model):
    __tablename__ = 'test_attempts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'), nullable=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    finished_at = db.Column(db.DateTime, nullable=True)
    score = db.Column(db.Float, nullable=True)
    ai_score = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(50), default='in_progress')

class QuestionAttempt(db.Model):
    __tablename__ = 'question_attempts'
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('test_attempts.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    response = db.Column(db.Text)
    time_spent_ms = db.Column(db.Integer, default=0)
    is_correct = db.Column(db.Boolean, nullable=True)
    ai_feedback = db.Column(JSON, nullable=True)
