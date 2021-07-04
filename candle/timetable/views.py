from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import current_user, login_required

from candle import db
from candle.models import UserTimetable, Lesson, Teacher, Room, StudentGroup
from candle.timetable.timetable import Timetable

timetable = Blueprint('timetable',
                      __name__,
                      template_folder='templates',
                      static_folder='static')


@timetable.route('/')
def home():
    if current_user.is_authenticated:
        user_timetables = current_user.timetables
        # if the user doesn't have any timetable:
        if user_timetables.first() is None:
            # create a new one:
            ut = UserTimetable(name='Rozvrh', user_id=current_user.id)
            db.session.add(ut)
            db.session.commit()
        else:
            # select the latest one (with the highest id):
            ut = user_timetables.order_by(UserTimetable.id_)[-1]

        # redirect to user's timetable view:
        return redirect(url_for('timetable.user_timetable', id_=ut.id_) )

    else:  # user is logged out, show welcome-info:
        return render_template('timetable/timetable.html', title='Rozvrh', show_welcome=True)


@timetable.route('/moj-rozvrh/<id_>')
@login_required
def user_timetable(id_):
    id_ = int(id_)
    user_timetables = current_user.timetables
    ut = UserTimetable.query.get_or_404(id_)
    if ut is None:
        return render_template('errors/404.html'), 404

    lessons = ut.lessons.order_by(Lesson.day, Lesson.start).all()
    t = Timetable(lessons)
    if t is None:
        raise Exception("Timetable cannot be None")
    return render_template('timetable/timetable.html',
                           title=ut.name, web_header=ut.name, timetable=t,
                           user_timetables=user_timetables, selected_timetable_key=id_,
                           show_welcome=False, editable=True)

