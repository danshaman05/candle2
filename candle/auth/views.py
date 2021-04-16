from flask import Blueprint, redirect, request, url_for, flash, current_app

from candle.models import User
from flask_login import login_user, logout_user
from functools import wraps


auth = Blueprint('auth', __name__)


def require_remote_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_app.config['DEBUG']:
            if request.environ.get('REMOTE_USER') is None:
                flash('User not logged in', 'error')
                return redirect(url_for('timetable.home'))
        return func(*args, **kwargs)
    return wrapper


@auth.route('/prihlasit', methods=['GET'])
@require_remote_user
def login():
    ais_login = request.environ.get('REMOTE_USER')
    user = User.query.filter_by(login=ais_login).first()
    if user:
        login_user(user, remember=True)  # defaultne si zapamatame usera, aby sa najblizsie nemusel zas prihlasovat
        #flash('Prihlasovanie prebehlo uspesne.')  # TODO (flash messages by boli krajsie ako nevypisat nic ...)

        #TODO mozno toto treba riesit cez "next" - co bude bezpecnejsie
        return redirect(request.referrer) if request.referrer else redirect(url_for("timetable.home"))

    else:
        ...
        #flash('Prihlasenie bolo neuspesne.')
        # TODO mozno lepsie je presmerovat / ukazat nejaku error page
    return redirect(request.referrer)   # vrati sa na stranku kde sme boli predtym


@auth.route('/odhlasit', methods=['GET'])
@require_remote_user
def logout():
    logout_user()
    # return redirect(request.referrer)
    return redirect(url_for('timetable.home'))
