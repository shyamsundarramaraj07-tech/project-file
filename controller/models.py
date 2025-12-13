# models.py
from controller.database import db

# --- existing base models (use as provided) ---
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)


class Role(db.Model):
    __tablename__ = 'roles'
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), unique=True, nullable=False)


class UserRole(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'), nullable=False)


# --- simple, clean quiz domain tables ---
class Subject(db.Model):
    __tablename__ = 'subjects'
    subject_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    description = db.Column(db.String(500), nullable=True)


class Quiz(db.Model):
    __tablename__ = 'quizzes'
    quiz_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.subject_id'), nullable=True)
    creator_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)  # teacher (User)
    total_marks = db.Column(db.Integer, nullable=True)
    is_published = db.Column(db.Boolean, default=False, nullable=False)
    start_time = db.Column(db.String(50), nullable=True)   # simple string timestamp if needed
    end_time = db.Column(db.String(50), nullable=True)
    allowed_duration_seconds = db.Column(db.Integer, nullable=True)


class Question(db.Model):
    __tablename__ = 'questions'
    question_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.quiz_id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(30), nullable=False, default='mcq_single')  # mcq_single, mcq_multiple, short
    marks = db.Column(db.Integer, nullable=False, default=1)
    position = db.Column(db.Integer, nullable=False, default=0)


class Choice(db.Model):
    __tablename__ = 'choices'
    choice_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.question_id'), nullable=False)
    text = db.Column(db.String(1000), nullable=False)
    is_correct = db.Column(db.Boolean, default=False, nullable=False)  # keep server-side only
    position = db.Column(db.Integer, nullable=False, default=0)


class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    enrollment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)   # student (User)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.subject_id'), nullable=False)
    __table_args__ = (db.UniqueConstraint('user_id', 'subject_id', name='uq_user_subject'),)


class Attempt(db.Model):
    __tablename__ = 'attempts'
    attempt_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.quiz_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)  # student (User)
    started_at = db.Column(db.String(50), nullable=True)
    submitted_at = db.Column(db.String(50), nullable=True)
    score = db.Column(db.Float, nullable=True)
    is_graded = db.Column(db.Boolean, default=False, nullable=False)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(300), nullable=True)


class Answer(db.Model):
    __tablename__ = 'answers'
    answer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('attempts.attempt_id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.question_id'), nullable=True)
    selected_choice_ids = db.Column(db.String(200), nullable=True)  # e.g. "1" or "2,5" - or use JSON if available
    text_response = db.Column(db.Text, nullable=True)
    marks_awarded = db.Column(db.Float, nullable=True)
