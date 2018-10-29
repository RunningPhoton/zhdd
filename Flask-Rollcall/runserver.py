# coding=UTF-8
# This Python file uses the following encoding: utf-8
# import os, random, string, binascii, json, pymysql, xlrd
# from flask import request, Response, abort, redirect, url_for, send_from_directory, session
# from Crypto.Cipher import AES

from rollcall.server import app
# @app.route('/')
# def index():
#     # 获得请求数据
#     verify_request = request.args.get('verify_request')
#     yb_uid = request.args.get('yb_uid')
#     # 解密数据
#     postStr = binascii.unhexlify(verify_request)
#     decryptor = AES.new(app.config['APPSECRET'].encode('utf-8'), AES.MODE_CBC, app.config['APPID'].encode('utf-8'))
#     info = json.loads(''.join([decryptor.decrypt(postStr).decode().strip().rsplit('}', 1)[0], '}']))
#     # 跳转授权界面
#     if info['visit_oauth'] == False:
#         return redirect('https://oauth.yiban.cn/code/html?client_id=' + app.config['APPID'] + '&redirect_uri=http://f.yiban.cn/iapp257395')
#     session['token'] = info['visit_oauth']['access_token']
#     session['uid'] = yb_uid
#     return 'Success'
#
# @app.route('/signup', methods = ['POST'])
# def login():
#     userType = request.form['userType'] # 用户类型
#     if 'tch' == userType:   # 用户类型 教师
#         # do something
#         return
#     elif 'stu' == userType: # 用户类型 学生
#         # do something
#         return
#     else:
#         return 'Error'
#     return 'Success'
#
# @app.route('/api/tch/manage')
# def tchManage():
#     tch = Teacher.query.filter_by(id = int(session.get('uid'))).first()
#     if not tch:
#         return 'error'
#     classes = {}
#     classes["id"] = tch.id
#     classes["classes"] = tch.classes.split(',')
#     return str(classes)
#
# @app.route('/api/tch/import', methods = ['GET', 'POST'])
# def tchImport():
#     if request.method == 'POST':
#         # 取得并暂时保存文件
#         file = request.files['file']
#         className = session['uid'] + '_' + file.filename
#         file.save('./tmp/' + className)
#         # 读取文件数据
#         table = xlrd.open_workbook('./tmp/' + className).sheets()[0]
#         stus = [table.cell_value(i, 0) for i in range(table.nrows)]
#         # 判断班级是否已存在
#         if Class.query.filter_by(name = className.replace('.xls', '')).first():
#             return 'Fail'
#         # 创建班级信息
#         classInfo = Class(className.replace('.xls', ''), json.dumps(stus, ensure_ascii=False), 0)
#         db.session.add(classInfo)
#         db.session.commit()
#         # 向教师数据条目追加班级
#         tch = Teacher.query.filter_by(id = int(session['uid'])).first()
#         classes = json.loads(tch.classes)
#         if (not tch) or className.replace('.xls', '') in classes:
#             return 'Fail'
#         classes.append(className.replace('.xls', ''))
#         tch.classes = json.dumps(classes, ensure_ascii=False)
#         db.session.commit()
#         # 删除文件
#         os.remove('./tmp/' + session['uid'] + '_' + file.filename)
#         return 'Success'
#
#     return '''
#     <!doctype html>
#     <title>Upload new File</title>
#     <h1>Upload new File</h1>
#     <form method=post enctype=multipart/form-data>
#       <input type=file name=file>
#       <input type=submit value=Upload>
#     </form>
#     '''
#
# @app.route('/api/tch/modify', methods = ['POST'])
# def tchModify():
#     className = request.form['classname']
#     stus = request.form['stus']
#     classInfo = Class.query.filter_by(classname = className).first()
#     if not classInfo:
#         return 'Error'
#     classInfo.stus = stus
#     db.session.commit()
#     return 'Success'
#
# @app.route('/api/tch/rollcall')
# def tchRollcall():
#     className = request.args.get('classname')
#     # 获得班级信息
#     classInfo = Class.query.filter_by(name = className).first()
#     classInfo.times += 1    # 已点名次数+1
#     # 新增一个点名
#     rollId = ''.join([random.choice(string.digits + string.ascii_letters) for i in range(12)])
#     result = [] # 点名结果
#     roll = Rollcall(rollId, className, classInfo.times, json.dumps(result))
#     db.session.add(roll)
#     # 设置点名
#     tch = Teacher.query.filter_by(id = int(session['uid'])).first()
#     tch.curroll = rollId
#     db.session.commit()
#     return rollId
#
# @app.route('/api/tch/endrollcall')
# def tchEndRollcall():
#     tch = Teacher.query.filter_by(id = int(session['uid'])).first()
#     tch.curroll = ''
#     db.session.commit()
#     return 'Success'
#
# @app.route('/api/stu/face', methods = ['POST'])
# def stuFace():
#     stu = Student.query.filter_by(id = int(session['uid'])).first()
#     stu.face = json.dumps([])
#     db.session.commit()
#     return 'Success'


if __name__ == '__main__':
    app.run()