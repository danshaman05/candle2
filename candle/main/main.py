from flask import Blueprint, redirect, url_for, render_template
from flask_login import current_user

from candle import db
from candle.models import UserTimetable

main = Blueprint('main',
                __name__,
                template_folder='templates',
                static_folder='static',
                static_url_path='/main/static'
                )

@main.route('/')
def home():
    if current_user.is_authenticated:
        my_timetables = current_user.timetables
        # if the user doesn't have any timetable:
        if my_timetables.first() is None:
            # create a new one:
            ut = UserTimetable(name='Rozvrh', user_id=current_user.id)
            db.session.add(ut)
            db.session.commit()
        else:
            # select the latest one (with the highest id):
            ut = my_timetables.order_by(UserTimetable.id_)[-1]
        # redirect to user's timetable view:
        return redirect(url_for('my_timetable.show_timetable', id_=ut.id_) )
    else:  # user is logged out, show welcome-info:
        return render_template('timetable/timetable.html', title='Rozvrh', show_welcome=True)