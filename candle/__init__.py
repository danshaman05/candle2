from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from candle.config import Config


login_manager = LoginManager()  # keeps session data
login_manager.login_view = 'auth.login'
# login_manager.login_message_category = 'info'  # flash message category (not yet implemented)

csrf = CSRFProtect()    # We need CSRF protection for our AJAX calls. More info: https://stackoverflow.com/questions/31888316/how-to-use-flask-wtforms-csrf-protection-with-ajax
db = SQLAlchemy()


# TODO Create an error module and move it there
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

    from candle.timetable.views import timetable
    from candle.rooms.views import rooms
    from candle.student_groups.views import student_groups
    from candle.teachers.views import teachers
    from candle.auth.views import auth
    from candle.timetable_manager.views import timetable_manager
    from candle.search.routes import search
    from candle.errors.handlers import errors

    app.register_blueprint(timetable, url_prefix=Config.SERVER_PATH)
    app.register_blueprint(rooms, url_prefix=Config.SERVER_PATH)
    app.register_blueprint(student_groups, url_prefix=Config.SERVER_PATH)
    app.register_blueprint(teachers, url_prefix=Config.SERVER_PATH)
    app.register_blueprint(auth, url_prefix=Config.SERVER_PATH)
    app.register_blueprint(timetable_manager, url_prefix=Config.SERVER_PATH)
    app.register_blueprint(search, url_prefix=Config.SERVER_PATH)
    app.register_blueprint(errors, url_prefix=Config.SERVER_PATH)

    return app
