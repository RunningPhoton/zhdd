# coding=UTF-8
# This Python file uses the following encoding: utf-8
import os
import time
from threading import Thread

from flask import request, g
from flask_cors import CORS
from sqlalchemy import func
from werkzeug.utils import secure_filename

from rollcall.tools import allowed_file, sign_by_figure, get_response, verify_email, send_async_email
from rollcall.utils import app, db
from model import User, File, Course, UserCourse, StudentSign, Sign
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

CORS(app, resources=r'/*')
# @app.route('/articles_list/contents/')
# def json_contents():
#     response = make_response(jsonify(response='success'))
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     response.headers['Access-Control-Allow-Methods'] = 'POST'
#     response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
#     return response



@app.route('/api/v1/test/', methods=['GET'])
def test():
    resp = {}
    msg = 'List coursesuccess'
    resp['msg'] = msg
    return get_response(resp)




@app.route('/api/v1/auth/sign_up/', methods=['POST'])
def sign_up():
    print(request.json)
    type = request.json.get('type') # 用户类型
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('mail')
    name = request.json.get('name')
    role = 1
    resp = {}
    msg = 'Register successful'
    if username is None or password is None:
        msg = 'Username and password can not be empty'
    elif(not verify_email(email)):
        msg = 'Email is Wrong'
    else:
        if User.query.filter_by(username=username).first() is not None:
            msg = 'The user already exists'
        else:
            if 'teacher' == type:
                role = 0
            user = User(username=username, name=name, role=role, mail=email)
            user.hash_password(password)
            db.session.add(user)
            db.session.commit()

    resp['msg'] = msg
    resp['role'] = role
    return get_response(resp)
    # return redirect(url_for('get_auth_token'))
@app.route('/api/v1/auth/send_email/', methods=['GET'])
def send_email():
    request.args.get('username')
    
    msg.body = '内容'
    thread = Thread(target=send_async_email, args=[app, msg])
    thread.start()
    return 'success'


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token

    # print(username_or_token)
    # print(password)
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

@app.route('/api/v1/auth/token/', methods=['GET'])
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    resp = {}
    resp['msg'] = 'Get token successful'
    resp['token'] = token.decode('ascii')
    resp['role'] = g.user.role
    return get_response(resp)

@app.route('/api/v1/tec/add_course/', methods=['POST'])
@auth.login_required
def add_course():
    code = request.json.get('code')
    name = request.json.get('name')
    location = request.json.get('location')
    time = request.json.get('time')

    resp = {}
    msg = 'Add course successful'
    if(g.user.role != 0):
        # abort(400)
        msg = 'User has no authority'
    elif(not code or not name or not location or not time):
        msg = 'Course message lost'
    else:
        course = Course(code=code, name=name, location=location, time=time, teacher_id=g.user.id)
        if(Course.query.filter_by(code=code).first() is not None):
            msg = 'The course already exists'
            # abort(400)
        else:
            db.session.add(course)
            db.session.commit()
    resp['msg'] = msg
    return get_response(resp)

@app.route('/api/v1/tec/list_courses/', methods=['GET'])
@auth.login_required
def list_courses():
    resp = {}
    resp['courses'] = []
    msg = 'List coursesuccess'
    user = g.user
    if(user.role != 0):
        msg = 'User has no authority'
    else:
        course = db.session.query(Course).filter_by(teacher_id=user.id).order_by(Course.create_at.desc()).limit(10)
        for data in course:
            k = {}
            k['id'] = data.id
            k['code'] = data.code
            k['name'] = data.name
            k['location'] = data.location
            k['time'] = data.time
            resp['courses'].append(k)
    resp['msg'] = msg
    return get_response(resp)

@app.route('/api/v1/tec/delete_course/', methods=['DELETE'])
@auth.login_required
def delete_course():
    course_id = int(request.args.get('course_id'))
    resp = {}
    msg = 'Delete successful'
    if(g.user.role != 0):
        msg = 'User has no authority'
    elif(db.session.query(Course).filter_by(id=course_id).first() is None):
        msg = 'There is no such course'
    else:
        signs = db.session.query(Sign).filter_by(course_id=course_id).all()

        for sign in signs:
            print(sign.id)
            delete_stu_sign = db.session.query(StudentSign).filter_by(sign_id=sign.id).delete()
        delete_sign = db.session.query(Sign).filter_by(course_id=course_id).delete()
        delete_user_course = db.session.query(UserCourse).filter_by(course_id=course_id).delete()
        delete_course = db.session.query(Course).filter_by(id=course_id).delete()
        db.session.commit()
    resp['msg'] = msg
    return get_response(resp)

@app.route('/api/v1/tec/sign/', methods=['POST'])
@auth.login_required
def sign():
    filename = request.json.get('filename')
    course_id = int(request.args.get('course_id'))
    print(filename)
    print(g.user.id)
    f = db.session.query(File).filter_by(name=filename).filter_by(user_id=g.user.id).first()
    msg = 'sign successful'
    resp = {}
    resp['miss'] = []
    if(not f):
        msg = 'There is no such file'
    elif(not course_id):
        msg = 'course_id is None'
    elif(db.session.query(Course).filter_by(id=course_id).first() is None):
        msg = 'There is no such course'
    elif(g.user.role != 0):
        msg = 'The user has no authority'
    else:
        file_url = f.url
        # find all students' ids who study in this course
        user_courses = db.session.query(UserCourse).filter_by(course_id=course_id).all()
        user_count = db.session.query(UserCourse).filter_by(course_id=course_id).count()
        sign_count = db.session.query(func.max(Sign.sign_count)).filter_by(course_id=course_id).first()
        print('signcount is {}'.format(sign_count))
        sign_count = sign_count[0]
        if(sign_count is None):
            sign_count = 1
        else:
            sign_count = sign_count + 1
        all_stu_ids = []
        urls = []
        ids = []
        for t in user_courses:
            f = db.session.query(File).filter_by(user_id=t.student_id).order_by(File.create_at.desc()).first()
            all_stu_ids.append(t.student_id)
            if not f:
                user = db.session.query(User).filter_by(id=t.student_id).first()
                resp['miss'].append({
                    'SID': user.username,
                    'name': user.name})
                continue
            ids.append(t.student_id)
            urls.append(f.url)

        sign_ids = sign_by_figure(ids, urls, file_url)
        sign = Sign(sign_count=sign_count, attendance=len(sign_ids), expectation=user_count, course_id=course_id)
        db.session.add(sign)
        db.session.commit()
        sign = db.session.query(Sign).filter_by(course_id=course_id).filter_by(sign_count=sign_count).first()

        for id in all_stu_ids:
            if(id in sign_ids):
                student_sign = StudentSign(student_id=id, sign_id=sign.id, status=0)
            elif(id in ids):
                student_sign = StudentSign(student_id=id, sign_id=sign.id, status=1)
            else:
                student_sign = StudentSign(student_id=id, sign_id=sign.id)
            db.session.add(student_sign)
        db.session.commit()
    resp['msg'] = msg
    return get_response(resp)


@app.route('/api/v1/tec/list_signs/', methods=['GET'])
@auth.login_required
def list_signs():
    course_id = int(request.args.get('course_id'))
    msg = 'list all signs successful'
    resp = {}
    resp['signs'] = []
    if(not course_id):
        msg = 'course_id is None'
    elif(g.user.role != 0):
        msg = 'User has no authority'
    elif(db.session.query(Course).filter_by(id=course_id).first() is None):
        msg = 'There is no such course'
    else:
        signs = db.session.query(Sign).filter_by(course_id=course_id).all()
        for t in signs:
            data = {}
            expectation = db.session.query(StudentSign).filter_by(sign_id=t.id).count()
            attendance = db.session.query(StudentSign).filter_by(sign_id=t.id).filter_by(status=0).count()
            t.attendance = attendance
            t.expectation = expectation
            data['sign_time'] = t.sign_count
            data['attendance'] = t.attendance
            data['expectation'] = t.expectation
            resp['signs'].append(data)
            db.session.commit()
    resp['msg'] = msg
    return get_response(resp)

@app.route('/api/v1/tec/list_signature/', methods=['GET'])
@auth.login_required
def list_signature():
    course_id = int(request.args.get('course_id'))
    sign_time = int(request.args.get('sign_time'))
    status = int(request.args.get('status'))
    resp = {}
    resp['students'] = []
    if(status == 1):
        msg = 'List unsigned students successful'
    elif(status == 0):
        msg = 'List signed students successful'
    else:
        msg = 'List unknown students successful'
    if(g.user.role != 0):
        msg = 'User has no authority'
    else:
        users = db.session.query(User).join(UserCourse).filter_by(course_id=course_id)\
            .join(StudentSign).filter_by(status=status).join(Sign).filter_by(sign_count=sign_time).all()
        for user in users:
            data = {}
            data['SID'] = user.username
            data['name'] = user.name
            resp['students'].append(data)
    resp['msg'] = msg
    return get_response(resp)

@app.route('/api/v1/tec/delete_signature/', methods=['DELETE'])
@auth.login_required
def delete_signature():
    course_id = int(request.args.get('course_id'))
    sign_time = int(request.args.get('sign_time'))
    resp = {}
    msg = 'Delete successful'
    if(g.user.role != 0):
        msg = 'User has no authority'
    elif(db.session.query(Course).filter_by(id=course_id).first() is None):
        msg = 'There is no such course'
    else:
        sign = db.session.query(Sign).filter_by(course_id=course_id).filter_by(sign_count=sign_time).first()
        if(sign is not None):
            delete_stu_sign = db.session.query(StudentSign).filter_by(sign_id=sign.id).delete()
            delete_sign = db.session.query(Sign).filter_by(course_id=course_id).filter_by(sign_count=sign_time).delete()
            db.session.commit()
    resp['msg'] = msg
    return get_response(resp)

@app.route('/api/v1/tec/add_student/', methods=['POST'])
@auth.login_required
def add_student():
    ids = request.json.get('ids')
    course_id = int(request.args.get('course_id'))
    print(ids, course_id)
    resp = {}
    msg = ''
    if(g.user.role != 0):
        msg = 'User has no authority'
    elif(not ids):
        msg = 'Message can not be empty'
    else:
        for id in ids:
            user = db.session.query(User).filter_by(username=id).first()
            if(not user or user.role == 0):
                msg = msg + '\nstudent NO: {} not exits'.format(id)
            elif(db.session.query(UserCourse).filter_by(student_id=user.id).first() is not None):
                msg = msg + '\nstudent NO: {} has exited in the class'.format(id)
            else:
                user_course = UserCourse(student_id=user.id,course_id=course_id)
                db.session.add(user_course)
                db.session.commit()
                msg = msg + '\nstudent NO : {} add successful'.format(id)
    resp['msg'] = msg
    return get_response(resp)

@app.route('/api/v1/tec/list_all_students/', methods=['GET'])
@auth.login_required
def list_all_students():
    course_id = int(request.args.get('course_id'))
    resp = {}
    resp['students'] = []
    msg = 'List all students successful'
    if(g.user.role != 0):
        msg = 'User has no authority'
    else:
        users = db.session.query(User).join(UserCourse).filter_by(course_id=course_id).all()
        for user in users:
            data = {}
            data['SID'] = user.username
            data['name'] = user.name
            resp['students'].append(data)
    resp['msg'] = msg
    return get_response(resp)

@app.route('/api/v1/tec/delete_student/', methods=['DELETE'])
@auth.login_required
def delete_student():
    course_id = int(request.args.get('course_id'))
    username = str(request.args.get('username'))
    print(course_id)
    print(username)
    resp = {}
    msg = 'Delete successful'
    if(g.user.role != 0):
        msg = 'User has no authority'
    elif(not username):
        msg = 'SID(username) can be none'
    elif(db.session.query(Course).filter_by(id=course_id).first() is None):
        msg = 'There is no such course'
    else:
        user = db.session.query(User).filter_by(username=username).first()
        signs = db.session.query(Sign).filter_by(course_id=course_id).all()
        if(user is not None and signs is not None):
            delete_user_course = db.session.query(UserCourse).filter_by(course_id=course_id).filter_by(student_id=user.id).delete()

            for sign in signs:
                delete_stu_sign = db.session.query(StudentSign).filter_by(student_id=user.id).filter_by(sign_id=sign.id).delete()
            db.session.commit()
    resp['msg'] = msg
    return get_response(resp)


@app.route('/api/v1/file/upload/', methods=['POST'])
@auth.login_required
def upload_file():
    user = g.user
    file = request.files['file']
    resp = {}
    resp['filename'] = ''
    msg = 'Upload successful'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        new_file = str(user.id) + '_' + user.username + '_' + str(int(time.time())) + '.' + filename.split('.')[1]
        basepath = os.path.dirname(__file__)
        if(user.role == 1):
            upload_path = os.path.join(basepath, app.config['UPLOAD_FOLDER_STU'], new_file)
        else:
            upload_path = os.path.join(basepath, app.config['UPLOAD_FOLDER_TEC'], new_file)
        file_url = upload_path
        file.save(upload_path)
        resp['filename'] = file_url.split('/')[-1]
        f = File(user_id=user.id, url=file_url, name=resp['filename'])
        db.session.add(f)
        db.session.commit()
    else:
        msg = 'Filename limitation'
    resp['msg'] = msg
    return get_response(resp)

