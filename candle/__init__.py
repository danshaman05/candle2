from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from candle.config import Config
from flask_jsglue import JSGlue

from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.wrappers import Response

login_manager = LoginManager()  # keeps session data
login_manager.login_view = 'auth.login'
# login_manager.login_message_category = 'info'  # flash message category (not yet implemented)

csrf = CSRFProtect()    # We need CSRF protection for our AJAX calls. More info: https://stackoverflow.com/questions/31888316/how-to-use-flask-wtforms-csrf-protection-with-ajax
db = SQLAlchemy()
jsglue = JSGlue()


def create_app(config_class=Config):
    app = Flask(__name__)

    # Use middleware for 2016 path-prefix. Used for testing.  Source: https://dlukes.github.io/flask-wsgi-url-prefix.html#mwe
    if app.config['ENV'] == "development":
        app.wsgi_app = DispatcherMiddleware(
            Response('Not Found', status=404),
            {'/2016-2017-zima': app.wsgi_app}
        )

    app.config.from_object(config_class)

    init_extensions(app)
    register_blueprints(app)

    return app


def register_blueprints(app):
    from candle.timetable.views import timetable
    from candle.rooms.views import rooms
    from candle.student_groups.views import student_groups
    from candle.teachers.views import teachers
    from candle.auth.views import auth
    from candle.timetable_manager.views import timetable_manager
    from candle.search.routes import search
    from candle.errors.handlers import errors

    app.register_blueprint(timetable)
    app.register_blueprint(rooms)
    app.register_blueprint(student_groups)
    app.register_blueprint(teachers)
    app.register_blueprint(auth)
    app.register_blueprint(timetable_manager)
    app.register_blueprint(search)
    app.register_blueprint(errors)


def init_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    app.jinja_env.add_extension('jinja2.ext.loopcontrols')
    app.jinja_env.add_extension('jinja2.ext.do')

    jsglue.init_app(app)