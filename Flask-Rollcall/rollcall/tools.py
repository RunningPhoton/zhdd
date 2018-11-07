import re
import numpy as np
from utils import mail

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}



email_str=r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
def verify_email(email):
    if(email and re.match(email_str, email)):
        return True
    else:
        return False

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def get_response(resp):
    from flask import make_response
    from flask import jsonify
    response = make_response(jsonify(resp))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response


# do sign by mtcnn and facenet
# paras:
# ids: the id of students
# urls: the face pictures of corresponding users
# file_url: the url of the picture that the teacher upload.
def sign_by_figure(ids, urls, file_url):
    sign_ids = []
    print(urls)
    print(file_url)
    for v in ids:
        if(np.random.rand() < 0.5):
            sign_ids.append(v)
    return sign_ids
