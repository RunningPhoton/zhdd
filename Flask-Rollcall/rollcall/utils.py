from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.from_object('rollcall.setting')
db = SQLAlchemy(app)
mail = Mail(app)