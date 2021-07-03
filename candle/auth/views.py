from flask import Blueprint, redirect, request, url_for, flash, current_app

from candle.models import User
from flask_login import login_user, logout_user
from functools import wraps


auth = Blueprint('auth', __name__)


def require_remote_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_app.config['ENV'] == 'production':
            if request.environ.get('REMOTE_USER') is None:
                flash('User not logged in', 'error')
                return redirect(url_for('timetable.home'))
        return func(*args, **kwargs)
    return wrapper


@auth.route('/prihlasit')
@require_remote_user
def login():
    ais_login = request.environ.get('REMOTE_USER')
    user = User.query.filter_by(login=ais_login).first()
    if user:
        login_user(user, remember=True)
        #flash('Prihlasovanie prebehlo uspesne.')

        return redirect(url_for("timetable.home"))

    else:
        ...
        #flash('Prihlasenie bolo neuspesne.')
        return redirect(url_for("timetable.home"))


@auth.route('/odhlasit')
@require_remote_user
def logout():
    logout_user()
    return redirect(url_for('timetable.home'))
