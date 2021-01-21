from flask import Blueprint, request, url_for, jsonify
from flask_login import current_user

from candle_backend import db
from ..models import UserTimetable

editable_timetable_manager = Blueprint('editable_timetable_manager', __name__)  # Blueprint instancia


@editable_timetable_manager.route("/new_timetable", methods=['POST'])
def new_timetable():
    name = request.form['data']
    ut = UserTimetable(name=name, user_id=current_user.id_)
    db.session.add(ut)
    db.session.commit()
    return url_for("timetable.user_timetable", id_=ut.id_)


@editable_timetable_manager.route("/delete_timetable", methods=['POST'])
def delete_timetable():
    url = request.form['data']
    id_ = int(url.split('/')[-1])   # id ziskame z URL

    ut = UserTimetable.query.get(id_)
    db.session.delete(ut)
    db.session.commit()

    # Ak uz nezostal ziaden rozvrh, tak vytvorime novy
    if len(list(current_user.timetables)) == 0:
        new_ut = UserTimetable(name="Rozvrh", user_id=current_user.id_)
        db.session.add(new_ut)
        db.session.commit()
        timetable_to_show_id = new_ut.id_
    else:
        # id naposledy pridaneho rozvrhu
        timetable_to_show_id = current_user.timetables.order_by(UserTimetable.id_)[-1].id_

    return jsonify({'next_url': url_for("timetable.user_timetable", id_=timetable_to_show_id)})
