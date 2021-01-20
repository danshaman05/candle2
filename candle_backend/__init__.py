from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# SERVER_PATH = '/2016-2017-zima'  # TODO - presunut do configuration.py
SERVER_PATH = ''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8aa7d5372cf499d28602959a6661e851'   # random string
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:SuperBakalarka1.@localhost/candle_2016_2017_zima'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MYSQL_DATABASE_CHARSET'] = 'utf8mb4'  # Kvoli collation - zatial nevyuzivame.
app.config['CSRF_ENABLED'] = True
# app.config['SQLALCHEMY_ECHO'] = True    # zobrazuje nam queries, kt. bezia na pozadi

app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.jinja_env.add_extension('jinja2.ext.do')

login_manager = LoginManager(app)   # udrziava session data v pozadi
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'   # flash message category (zatial nepotrebujeme) - v Bootstrap je to pekne modre upozornenie


db = SQLAlchemy(app)


from candle_backend.timetable.views import timetable  # importujeme instanciu main
from candle_backend.rooms.views import rooms
from candle_backend.student_groups.views import student_groups
from candle_backend.teachers.views import teachers
from candle_backend.users.views import users
from candle_backend.editable_timetable_manager.views import editable_timetable_manager

app.register_blueprint(timetable, url_prefix=SERVER_PATH)
app.register_blueprint(rooms, url_prefix=SERVER_PATH)
app.register_blueprint(student_groups, url_prefix=SERVER_PATH)
app.register_blueprint(teachers, url_prefix=SERVER_PATH)
app.register_blueprint(users, url_prefix=SERVER_PATH)
app.register_blueprint(editable_timetable_manager, url_prefix=SERVER_PATH)
