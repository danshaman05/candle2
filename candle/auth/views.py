from flask import Blueprint, redirect, request, url_for

from candle.models import User
from flask_login import login_user, logout_user, current_user


auth = Blueprint('auth', __name__)



@auth.route('/prihlasit', methods=['GET'])
def login():
    ais_login = 'grohol2'  # TODO treba implementovat CoSign prihlasenie cez AIS ('grohol2' je moj AIS login)
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
def logout():
    logout_user()
    # return redirect(request.referrer)
    return redirect(url_for('timetable.home'))
