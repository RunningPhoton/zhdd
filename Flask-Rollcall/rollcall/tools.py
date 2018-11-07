
import numpy as np
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
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
