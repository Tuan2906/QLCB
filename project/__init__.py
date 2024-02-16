from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_admin import Admin
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = "@@@@@@@"  # khong bi loi cho add
# cau hinh ket noi voi mysql
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:%s@localhost/qlcb' % quote('ngoquang178')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app=app)
admin = Admin(app=app, name="QUẢN LÝ CHUYẾN BAY", template_mode="bootstrap4")
login = LoginManager(app=app)
