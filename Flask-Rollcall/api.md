# Documentation
API遵循RESTful规范。
---

## 学生端(role=1)

## 注册[/api/v1/auth/sign_up/] methods=['POST']

###Header
Content-Type = application/json

###Body
{
  "type": "teacher",
  "username": "2",
  "password": "123",
  "name": "huangyuxiao"
}
###Response
成功返回：
{
    "msg": "Register successful",
    "role": 1
}
失败返回:
{
    "msg": "The user already exists",
    "role": 1
}

## 获取token验证码(登录)[/api/v1/auth/token/] methods=['GET']

###Header
Authorization: Basic Auth (用户名填token或者学工号，在用户名不为token时，需要填密码)
认证失败返回: "Unauthorized Access"

###Body

###Response
成功返回：
{
    "msg": "Get token successful",
    "role": 1,
    "token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTU0MDc5ODc5MCwiaWF0IjoxNTQwNzk4MTkwfQ.eyJpZCI6MX0.fjQ103QnfhMyPr-yeLOG3aHcKUJPqlr0pm_8ep0pvcw"
}

## 文件上传[/api/v1/file/upload/] methods=['POST']

###Header

Content-Type = application/json

Authorization: Basic Auth (用户名填token或者学工号，在用户名不为token时，需要填密码)
认证失败返回: "Unauthorized Access"

###Body
file: <file>
###Response
成功返回：
{
    "filename": "3_5_1540788548.jpg",
    "msg": "Upload successful"
}


## 教师端(role=0)

## 注册[/api/v1/auth/sign_up/] methods=['POST']

###Header
Content-Type = application/json

###Body
{
  "type": "teacher",
  "username": "2",
  "password": "123",
  "name": "huangyuxiao"
}
###Response
成功返回：
{
    "msg": "Register successful",
    "role": 0
}
失败返回:
{
    "msg": "The user already exists",
    "role": 0
}

## 获取token验证码(登录)[/api/v1/auth/token/] methods=['GET']

###Header
Authorization: Basic Auth (用户名填token或者学工号，在用户名不为token时，需要填密码)
认证失败返回: "Unauthorized Access"

###Body

###Response
成功返回：
{
    "msg": "Get token successful",
    "role": 0,
    "token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTU0MDc5ODc5MCwiaWF0IjoxNTQwNzk4MTkwfQ.eyJpZCI6MX0.fjQ103QnfhMyPr-yeLOG3aHcKUJPqlr0pm_8ep0pvcw"
}

## 文件上传[/api/v1/file/upload/] methods=['POST']

###Header

Content-Type = application/json

Authorization: Basic Auth (用户名填token或者学工号，在用户名不为token时，需要填密码)
认证失败返回: "Unauthorized Access"

###Body
file: <file>
###Response
成功返回：
{
    "filename": "3_5_1540788548.jpg",
    "msg": "Upload successful"
}

## 添加课程[/api/v1/tec/add_course/] methods=['POST']

###Header

Content-Type = application/json

Authorization: Basic Auth (用户名填token或者学工号，在用户名不为token时，需要填密码)
认证失败返回: "Unauthorized Access"

###Body
{
    "code": "UUDAS3",
    "name": "数学3",
    "location": "A5401",
    "time": "1,3,5周第7-8节"
}
###Response
成功返回:
{
    "msg": "Add course successful"
}
失败返回:
{
    "msg": "The course already exists"
}

## 查看该教师（当前用户）所有课程[/api/v1/tec/list_courses/] methods=['GET']

###Header


Authorization: Basic Auth (用户名填token或者学工号，在用户名不为token时，需要填密码)
认证失败返回: "Unauthorized Access"

###Body

###Response
成功返回:
{
    "courses": [
        {
            "code": "UUDAS3",
            "id": 3,
            "location": "A5401",
            "name": "数学3",
            "time": "1,3,5周第7-8节"
        },
        {
            "code": "UUDAS2",
            "id": 2,
            "location": "A5401",
            "name": "数学2",
            "time": "1,3,5周第7-8节"
        }
    ],
    "msg": "List coursesuccess"
}
失败返回:


## 按照学号添加学生到该课程[/api/v1/tec/add_student/<course_id>] methods=['POST']

###url params
course_id = 2

###Header

Content-Type = application/json

Authorization: Basic Auth (用户名填token或者学工号，在用户名不为token时，需要填密码)
认证失败返回: "Unauthorized Access"

###Body
{
  "ids": ["3","4","5","6","7","8","9","10","11"]
}
###Response
成功返回:
{
    "msg": "\nstudent NO : 3 add successful\nstudent NO: 4 has exited in the class\nstudent NO: 5 has exited in the class\nstudent NO: 6 has exited in the class\nstudent NO: 7 has exited in the class\nstudent NO: 8 has exited in the class\nstudent NO: 9 has exited in the class\nstudent NO: 10 has exited in the class\nstudent NO: 11 not exits"
}
失败返回:
{
    "msg": "The course already exists"
}

## 列出该课程所有学生[/api/v1/tec/list_all_students/<course_id>] methods=['GET']

###url params
course_id = 2

###Header

Authorization: Basic Auth (用户名填token或者学工号，在用户名不为token时，需要填密码)
认证失败返回: "Unauthorized Access"


###Body

###Response
成功返回:
{
    "msg": "List all students successful",
    "students": [
        {
            "SID": "3",
            "name": "huangyuxiao"
        },
        {
            "SID": "4",
            "name": "huangyuxiao"
        },
        {
            "SID": "5",
            "name": "huangyuxiao"
        },
        {
            "SID": "6",
            "name": "huangyuxiao"
        },
        {
            "SID": "7",
            "name": "huangyuxiao"
        },
        {
            "SID": "8",
            "name": "huangyuxiao"
        },
        {
            "SID": "9",
            "name": "huangyuxiao"
        },
        {
            "SID": "10",
            "name": "huangyuxiao"
        }
    ]
}
失败返回:
{
    "msg": "List all students successful",
    "students": []
}


## 发起签到[/api/v1/tec/sign/<course_id>] methods=['POST']

###url params
course_id = 2

###Header

Content-Type = application/json

Authorization: Basic Auth (用户名填token或者学工号，在用户名不为token时，需要填密码)
认证失败返回: "Unauthorized Access"



###Body
{
  "filename": "9_1_1540780437.jpg"
}
###Response
注意：miss表示该学生未上传照片，无法完成识别
成功返回:
{
    "miss": [
        {
            "SID": "6",
            "name": "huangyuxiao"
        },
        {
            "SID": "7",
            "name": "huangyuxiao"
        },
        {
            "SID": "8",
            "name": "huangyuxiao"
        },
        {
            "SID": "9",
            "name": "huangyuxiao"
        },
        {
            "SID": "10",
            "name": "huangyuxiao"
        }
    ],
    "msg": "sign successful"
}
失败返回:
{
    "miss": [],
    "msg": "There is no such course"
}

## 列出该课程的签到情况[/api/v1/tec/list_signs/<course_id>] methods=['GET']

###url params
course_id = 2

###Header

Content-Type = application/json

Authorization: Basic Auth (用户名填token或者学工号，在用户名不为token时，需要填密码)
认证失败返回: "Unauthorized Access"

###Body
###Response
注意：attendance表示出勤人数，expectation表示总人数，sign_time表示是第几次签到
成功返回:
{
    "msg": "list all signs successful",
    "signs": [
        {
            "attendance": 2,
            "expectation": 7,
            "sign_time": 1
        },
        {
            "attendance": 2,
            "expectation": 7,
            "sign_time": 2
        }
    ]
}
失败返回:
{
    "msg": "There is no such course",
    "signs": []
}


## 查看该课程第<sign_time>次的签到情况[/api/v1/tec/list_signature/<course_id><sign_time><status>] methods=['GET']

###url params
course_id = 3
sign_time = 1
status = 0(出席的), 1(没到的), 2(其他，多半是没上传自己照片的呆学生)
###Header

Content-Type = application/json

Authorization: Basic Auth (用户名填token或者学工号，在用户名不为token时，需要填密码)
认证失败返回: "Unauthorized Access"

###Body

###Response
成功返回:
{
    "msg": "List unsigned students successful",
    "students": [
        {
            "SID": "3",
            "name": "huangyuxiao"
        },
        {
            "SID": "5",
            "name": "huangyuxiao"
        }
    ]
}
成功返回:
{
    "msg": "List signed students successful",
    "students": []
}
成功返回:
{
    "msg": "List unknown students successful",
    "students": []
}
失败返回:


## 删除第<sign_time>次的签到[/api/v1/tec/delete_signature/<course_id><sign_time>] methods=['DELETE']

###url params
course_id = 3
sign_time = 2

###Header

Content-Type = application/json

Authorization: Basic Auth (用户名填token或者学工号，在用户名不为token时，需要填密码)
认证失败返回: "Unauthorized Access"

###Body
###Response
成功返回:
{
    "msg": "Delete successful"
}
失败返回:



## 删除id为<course_id>的课程[/api/v1/tec/delete_course/<course_id>] methods=['DELETE']

###url params
course_id = 3

###Header

Content-Type = application/json

Authorization: Basic Auth (用户名填token或者学工号，在用户名不为token时，需要填密码)
认证失败返回: "Unauthorized Access"

###Body
###Response
成功返回:
{
    "msg": "Delete successful"
}
失败返回:

## 在id为<course_id>的课程中删除学号为<username>的人[/api/v1/tec/delete_student/<course_id><username>] methods=['DELETE']

###url params
course_id = 3
username = "3"
###Header

Content-Type = application/json

Authorization: Basic Auth (用户名填token或者学工号，在用户名不为token时，需要填密码)
认证失败返回: "Unauthorized Access"

###Body
###Response
成功返回:
{
    "msg": "Delete successful"
}
失败返回: