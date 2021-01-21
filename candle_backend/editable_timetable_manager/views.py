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
    # if etm.get_timetables_count() < 2:  # TODO zmazat .. a zmenit aj JQUERY funkciu!
    #     return jsonify({'error': "Operácia neúspešná! Zostal už len jeden rozvrh, pre jeho zmazanie musíte vytvoriť ďalší."})

    url = request.form['data']
    key = int(url.split('/')[-1])   # ziskame timetable key, kt. treba zmazat

    editable_timetable = etm.get_timetable(key)
    db.session.delete(editable_timetable.timetable)
    db.session.commit()

    etm.delete_timetable(key)
    next_timetable_key = etm.get_max_key()
    # TODO POUZIT NIECO TAKE: ... new_key = current_user.timetables.order_by(UserTimetable.id_)


    return jsonify({'next_url': url_for("timetable.user_timetable", key=next_timetable_key)})
