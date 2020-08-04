from flask import Blueprint, redirect, url_for, flash, request

from candle_backend.models import User
from flask_login import login_user, logout_user

from .. import temporary_path   # TODO presunut do config filu


users = Blueprint('users', __name__)  # Blueprint instancia


@users.route(temporary_path + '/prihlasit', methods=['GET'])
def login():
    ais_login = 'grohol2'  # TODO treba implementovat CoSign prihlasenie cez AIS ('grohol2' je moj AIS login)
    user = User.query.filter_by(login=ais_login).first()
    if user:
        login_user(user, remember=True)  # defaultne si zapamatame usera, aby sa najblizsie nemusel zas prihlasovat
        #flash('Prihlasovanie prebehlo uspesne.')  # TODO (flash messages by boli krajsie ako nevypisat nic ...)
        return redirect(request.referrer)
    else:
        #flash('Prihlasenie bolo neuspesne.')
        # TODO mozno lepsie je presmerovat / ukazat nejaku error page
        return redirect(request.referrer)   # vrati sa na stranku kde sme boli predtym


@users.route(temporary_path + '/odhlasit', methods=['GET'])
def logout():
    logout_user()
    return redirect(request.referrer)
