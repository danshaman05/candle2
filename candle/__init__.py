'''
Project: Candle (New Generation): Candle rewrite from PHP to Python.
Author: Daniel Grohol
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from candle.config import Config
from flask_jsglue import JSGlue

from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.wrappers import Response


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Use middleware for 2016 path-prefix. Used for testing.  Source: https://dlukes.github.io/flask-wsgi-url-prefix.html#mwe
    if app.config['ENV'] == "development":
        app.wsgi_app = DispatcherMiddleware(
            Response('Not Found', status=404),
            {'/2016-2017-zima': app.wsgi_app}
        )

    init_extensions(app)
    register_blueprints(app)
    return app


def register_blueprints(app):
    from candle.main.main import main
    from candle.api.api import api
    from candle.auth.auth import auth
    from candle.timetable.timetable import timetable
    from candle.my_timetable.my_timetable import my_timetable
    from candle.entities.room.room import room
    from candle.entities.student_group.student_group import student_group
    from candle.entities.teacher.teacher import teacher
    from candle.panel.panel import panel
    from candle.search.search import search
    from candle.errors.errors import errors

    app.register_blueprint(main)
    app.register_blueprint(api)
    app.register_blueprint(auth)
    app.register_blueprint(timetable)
    app.register_blueprint(my_timetable)
    app.register_blueprint(room)
    app.register_blueprint(student_group)
    app.register_blueprint(teacher)
    app.register_blueprint(panel)
    app.register_blueprint(search)
    app.register_blueprint(errors)


def init_extensions(app):
    csrf = CSRFProtect()  # We need CSRF protection for our AJAX calls. More info: https://stackoverflow.com/questions/31888316/how-to-use-flask-wtforms-csrf-protection-with-ajax

    db = SQLAlchemy()
    db.init_app(app)

    login_manager = LoginManager()  # keeps session data
    # login_manager.login_message_category = 'info'  # flash message category (not yet implemented)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    csrf.init_app(app)

    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    app.jinja_env.add_extension('jinja2.ext.loopcontrols')
    app.jinja_env.add_extension('jinja2.ext.do')

    jsglue = JSGlue()
    jsglue.init_app(app)
