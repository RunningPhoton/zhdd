# coding=UTF-8
# This Python file uses the following encoding: utf-8
import datetime
from sqlalchemy import ForeignKey
from passlib.apps import custom_app_context as pwd_context
from rollcall.utils import db, app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(30), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(20), index=True)
    role = db.Column(db.Integer, default=1, index=True)
    verify = db.Column(db.Integer, default=1)
    create_at = db.Column(db.DateTime, default=datetime.datetime.now)
    def __init__(self, username, name, role, id=None, password_hash=None, verify=None, create_at=None):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.name = name
        self.role = role
        self.verify = verify
        self.create_at = create_at

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    code = db.Column(db.String(30), index=True, unique=True)
    name = db.Column(db.String(30))
    location = db.Column(db.String(30))
    time = db.Column(db.String(50))
    teacher_id = db.Column(db.Integer, ForeignKey("users.id"), nullable=True, index=True)
    create_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, code, name, location, time, teacher_id, id=None, create_at=None):
        self.id = id
        self.code = code
        self.name = name
        self.location = location
        self.time = time
        self.teacher_id = teacher_id
        self.create_at = create_at

class UserCourse(db.Model):
    __tablename__ = 'user_courses'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    student_id = db.Column(db.Integer, ForeignKey("users.id"), index=True)
    course_id = db.Column(db.Integer, ForeignKey("courses.id"), index=True)
    create_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, student_id, course_id, id=None, creat_at=None):
        self.id = id
        self.student_id = student_id
        self.course_id = course_id
        self.create_at = creat_at

class Sign(db.Model):
    __tablename__ = 'signs'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    sign_count = db.Column(db.Integer, index=True, default=0)
    attendance = db.Column(db.Integer, default=0)
    expectation = db.Column(db.Integer, default=0)
    course_id = db.Column(db.Integer, ForeignKey("courses.id"), nullable=False, index=True)
    create_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, sign_count, attendance, expectation, course_id, id=None, creat_at=None):
        self.id = id
        self.sign_count = sign_count
        self.attendance = attendance
        self.expectation = expectation
        self.course_id = course_id
        self.create_at = creat_at

class StudentSign(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    student_id = db.Column(db.Integer, ForeignKey("users.id"), index=True)
    sign_id = db.Column(db.Integer, ForeignKey("signs.id"), index=True)
    # 0代表成功签到，1代表签到失败，2代表未知状态
    status = db.Column(db.Integer, index=True, default=2)
    create_at = db.Column(db.DateTime, default=datetime.datetime.now)


    def __init__(self, student_id, sign_id, id=None, status=None, create_at=None):
        self.id = id
        self.student_id = student_id
        self.sign_id = sign_id
        self.status = status
        self.create_at = create_at

class File(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("users.id"), nullable=False, index=True)
    url = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(50), nullable=False, index=True, unique=True)
    create_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, user_id, url, name,id=None, creat_at=None):
        self.id = id
        self.user_id = user_id
        self.url = url
        self.name = name
        self.create_at = creat_at