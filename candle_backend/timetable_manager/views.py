from flask import Blueprint, request, url_for, jsonify
from flask_login import current_user

from candle_backend import db
from ..models import UserTimetable, Teacher, Room, StudentGroup

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
    """ Priklady URL:
     /ucitelia/Stanislav-Antalic
     /miestnosti/B1-302
     /kruzky/1mFAA
     /moj-rozvrh/751
    """

    url_list = rozvrh_url.split('/')

    if "ucitelia" in url_list:
        i = url_list.index("ucitelia")
        slug = url_list[i + 1]    # pozicia ucitelovho slugu v url
        teacher = Teacher.query.filter_by(slug=slug).first_or_404()  # podla slugu najdeme ucitela
        new_t = UserTimetable(name=teacher.short_name, user_id=current_user.id)
        db.session.add(new_t)
        for lesson in teacher.lessons:
            new_t.lessons.append(lesson)
        db.session.commit()
        return jsonify({'next_url': url_for("timetable.user_timetable", id_=new_t.id_)})

    if "miestnosti" in url_list:
        i = url_list.index("miestnosti")
        name = url_list[i + 1]
        room = Room.query.filter_by(name=name).first_or_404()
        new_t = UserTimetable(name=name, user_id=current_user.id)
        db.session.add(new_t)
        for lesson in room.lessons:
            new_t.lessons.append(lesson)
        db.session.commit()
        return jsonify({'next_url': url_for("timetable.user_timetable", id_=new_t.id_)})

    if "kruzky" in url_list:
        i = url_list.index("kruzky")
        name = url_list[i + 1]
        student_group = StudentGroup.query.filter_by(name=name).first_or_404()
        new_t = UserTimetable(name=name, user_id=current_user.id)
        db.session.add(new_t)
        for lesson in student_group.lessons:
            new_t.lessons.append(lesson)
        db.session.commit()
        return jsonify({'next_url': url_for("timetable.user_timetable", id_=new_t.id_)})


    if "moj-rozvrh" in url_list:
        i = url_list.index("moj-rozvrh")
        id = url_list[i + 1]
        print("ID: " + id)
        user_timetable = UserTimetable.query.get(id)
        new_t = UserTimetable(name=user_timetable.name, user_id=current_user.id)
        db.session.add(new_t)
        for lesson in user_timetable.lessons:
            new_t.lessons.append(lesson)
        db.session.commit()
        return jsonify({'next_url': url_for("timetable.user_timetable", id_=new_t.id_)})








