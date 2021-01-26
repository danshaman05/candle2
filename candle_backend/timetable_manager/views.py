from flask import Blueprint, request, url_for, jsonify
from flask_login import current_user

from candle_backend import db
from ..models import UserTimetable, Teacher

timetable_manager = Blueprint('editable_timetable_manager', __name__)  # Blueprint instancia


@timetable_manager.route("/new_timetable", methods=['POST'])
def new_timetable():
    name = request.form['data']
    ut = UserTimetable(name=name, user_id=current_user.id)
    db.session.add(ut)
    db.session.commit()
    return url_for("timetable.user_timetable", id_=ut.id_)


@timetable_manager.route("/delete_timetable", methods=['POST'])
def delete_timetable():
    rozvrh_url = request.form['data']
    id_ = int(rozvrh_url.split('/')[-1])   # id ziskame z URL

    ut = UserTimetable.query.get(id_)
    db.session.delete(ut)
    db.session.commit()

    # Ak uz nezostal ziaden rozvrh, tak vytvorime novy
    if len(list(current_user.timetables)) == 0:
        new_ut = UserTimetable(name="Rozvrh", user_id=current_user.id)
        db.session.add(new_ut)
        db.session.commit()
        timetable_to_show_id = new_ut.id_
    else:
        # id naposledy pridaneho rozvrhu
        timetable_to_show_id = current_user.timetables.order_by(UserTimetable.id_)[-1].id_
    return jsonify({'next_url': url_for("timetable.user_timetable", id_=timetable_to_show_id)})

@timetable_manager.route("/duplicate_timetable", methods=['POST'])
def duplicate_timetable():
    rozvrh_url = request.form['data']
    """ Mozne url:
     /ucitelia/Stanislav-Antalic
     /miestnosti/B1-302
     /kruzky/1mFAA
     /moj/rozvrh/751
    """

    print("URL: " + rozvrh_url)
    url_list = rozvrh_url.split('/')
    if "ucitelia" in url_list:
        i = url_list.index("ucitelia")
        slug = url_list[i+1]
        #podla slugu najdeme ucitela
        teacher = Teacher.query.filter_by(slug=slug).first_or_404()
        name = teacher.short_name
        #vytvorime userovi novy t. podla lessons daneho ucitela
        ut = UserTimetable(name=name, user_id=current_user.id)
        db.session.add(ut)
        for lesson in teacher.lessons:
            ut.lessons.append(lesson)
        db.session.commit()
        return jsonify({'next_url': url_for("timetable.user_timetable", id_=ut.id_)})

    # if "miestnosti" in url_list:
    #     # TODO
    #     ...





