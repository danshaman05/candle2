from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:SuperBakalarka1.@localhost/candle_2016_2017_zima'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MYSQL_DATABASE_CHARSET'] = 'utf8mb4'  # Kvoli collation - zatial nevyuzivame.

app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.jinja_env.add_extension('jinja2.ext.do')

db = SQLAlchemy(app)


temporary_path = '/2016-2017-zima' # TODO - presunut do configuration.py


from candle_backend.main.routes import main  # importujeme instanciu main
from candle_backend.rooms.routes import rooms
from candle_backend.student_groups.routes import student_groups
from candle_backend.teachers.routes import teachers

app.register_blueprint(main)
app.register_blueprint(rooms)
app.register_blueprint(student_groups)
app.register_blueprint(teachers)