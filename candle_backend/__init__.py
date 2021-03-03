from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect, \
    CSRFError  # https://stackoverflow.com/questions/31888316/how-to-use-flask-wtforms-csrf-protection-with-ajax
from candle_backend.config import Config


login_manager = LoginManager()  # udrziava session data v pozadi
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'  # flash message category (zatial nepotrebujeme) - v Bootstrap je to pekne modre upozornenie

csrf = CSRFProtect()
db = SQLAlchemy()


# # TODO presunut do samostatneho modulu errors
# @app.errorhandler(CSRFError)
# def csrf_error(reason):
#     return render_template('errors/csrf_error.html', reason=reason)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    app.jinja_env.add_extension('jinja2.ext.loopcontrols')
    app.jinja_env.add_extension('jinja2.ext.do')

    from candle_backend.timetable.views import timetable  # importujeme instanciu main
    from candle_backend.rooms.views import rooms
    from candle_backend.student_groups.views import student_groups
    from candle_backend.teachers.views import teachers
    from candle_backend.auth.views import auth
    from candle_backend.timetable_manager.views import timetable_manager
    app.register_blueprint(timetable, url_prefix=Config.SERVER_PATH)
    app.register_blueprint(rooms, url_prefix=Config.SERVER_PATH)
    app.register_blueprint(student_groups, url_prefix=Config.SERVER_PATH)
    app.register_blueprint(teachers, url_prefix=Config.SERVER_PATH)
    app.register_blueprint(auth, url_prefix=Config.SERVER_PATH)
    app.register_blueprint(timetable_manager, url_prefix=Config.SERVER_PATH)

    return app
