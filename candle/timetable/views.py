from flask import Blueprint, render_template
from flask_login import current_user, login_required

from candle import db
from ..models import UserTimetable, Lesson
from ..timetable.Timetable import Timetable

timetable = Blueprint('timetable', __name__)


@timetable.route('/moj-rozvrh/<id_>', methods=['GET'])
@login_required
def user_timetable(id_):
    id_ = int(id_)
    user_timetables = current_user.timetables
    ut = UserTimetable.query.get(id_)
    lessons = ut.lessons.order_by(Lesson.day, Lesson.start).all()
    t = Timetable(lessons)
    if timetable is None:
        raise Exception("timetable cannot be None")

    return render_template('timetable/timetable.html',
                           title=ut.name, web_header=ut.name,
                           timetable=t,
                           user_timetables=user_timetables, selected_timetable_key=id_)


@timetable.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        user_timetables = current_user.timetables
        # if the user doesn't have any timetable:
        if user_timetables.first() is None:
            # create a new one:
            user_timetable = UserTimetable(name='Rozvrh', user_id=current_user.id)
            db.session.add(user_timetable)
            db.session.commit()
        else:
            # select the latest one (with the highest id):
            user_timetable = user_timetables.order_by(UserTimetable.id_)[-1]
        timetable = Timetable(user_timetable.lessons)
        if timetable is None:
            raise Exception("timetable cannot be None")
        # show timetable:
        return render_template('timetable/timetable.html',
                               title=user_timetable.name, web_header=user_timetable.name,
                               timetable=timetable,
                               user_timetables=current_user.timetables,
                               selected_timetable_key=user_timetable.id_,
                               infobox=False)
    else:  # user is logged out, show infobox:
        return render_template('timetable/timetable.html',
                               title='Rozvrh',
                               infobox=True)    # prints out Infobox
