# coding=UTF-8
# This Python file uses the following encoding: utf-8
DEBUG = True

# session
SECRET_KEY = '5ff18140047ab1302b1928f36ee04250'

# mysql database
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:hyx@localhost:3306/zhdd'
SQLALCHEMY_COMMIT_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_COMMIT_ON_TEARDOWN = True

# yiban
APPID = 'd412b3d1c0f03d03'
APPSECRET = '5ff18140047ab1302b1928f36ee04250'

# file limitation
UPLOAD_FOLDER_STU = 'students/'
UPLOAD_FOLDER_TEC = 'teachers/'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}