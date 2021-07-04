import re
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
    ut = UserTimetable.query.get(id_)
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


@timetable.route('/moj-rozvrh', methods=['POST'])
@login_required
def new_timetable():
    """Create a new timetable"""
    name = request.form['name']
    name = getUniqueName(name)
    ut = UserTimetable(name=name, user_id=current_user.id)
    db.session.add(ut)
    db.session.commit()
    return url_for("timetable.user_timetable", id_=ut.id_)


@login_required
@timetable.route("/ucitelia/<teacher_slug>/duplicate", methods=['POST'])
def duplicate_teacher_timetable(teacher_slug):
    old_timetable = Teacher.query.filter_by(slug=teacher_slug).first_or_404()
    new_timetable_id = duplicate_timetable(old_timetable)
    return jsonify({'next_url': url_for("timetable.user_timetable", id_=new_timetable_id)})

@login_required
@timetable.route("/miestnosti/<room_url_id>/duplicate", methods=['POST'])
def duplicate_room_timetable(room_url_id):
    old_timetable = Room.query.filter_by(name=room_url_id).first_or_404()
    new_timetable_id = duplicate_timetable(old_timetable)
    return jsonify({'next_url': url_for("timetable.user_timetable", id_=new_timetable_id)})

@login_required
@timetable.route("/kruzky/<group_url_id>/duplicate", methods=['POST'])
def duplicate_student_group_timetable(group_url_id):
    old_timetable = StudentGroup.query.filter_by(name=group_url_id).first_or_404()
    new_timetable_id = duplicate_timetable(old_timetable)
    return jsonify({'next_url': url_for("timetable.user_timetable", id_=new_timetable_id)})

@login_required
@timetable.route("/moj-rozvrh/<id_>/duplicate", methods=['POST'])
def duplicate_my_timetable(id_):
    old_timetable = UserTimetable.query.get(id_)
    new_timetable_id = duplicate_timetable(old_timetable)
    return jsonify({'next_url': url_for("timetable.user_timetable", id_=new_timetable_id)})


def duplicate_timetable(old_timetable):
    """Create a new timetable as a duplicate of old one and return its id."""
    if isinstance(old_timetable, Teacher):
        old_name = old_timetable.short_name
    else:
        old_name = old_timetable.name
    new_name = getUniqueName(old_name)
    new_t = UserTimetable(name=new_name, user_id=current_user.id)
    db.session.add(new_t)
    for lesson in old_timetable.lessons:
        new_t.lessons.append(lesson)
    db.session.commit()
    return new_t.id_


def getUniqueName(name) -> str:
    """Ensure that this timetable will not have the same name as some other one.
    :param name: name for timetable
    :return: unique name for timetable
    """
    pattern = '^(.*) \(\d+\)$'
    match = re.match(pattern, name)
    # if the name is in the format "Name (x)", where x is a number:
    if match:
        name = match.group(1)  # get the name before parenthesis (without a number)

    # get the names of the current timetables:
    timetables_names = [t.name for t in current_user.timetables]

    if name not in timetables_names:
        return name

    # add "(index)" after the name, and try if it is unique:
    index = 2
    while True:
        new_name = f"{name} ({index})"
        if new_name not in timetables_names:
            return new_name
        index += 1


@login_required
@timetable.route("/moj-rozvrh/<id_>/delete", methods=['DELETE'])
def delete_timetable(id_):
    ut = UserTimetable.query.get_or_404(id_)
    db.session.delete(ut)
    db.session.commit()

    # if there is no timetable left, create a new one:
    if len(list(current_user.timetables)) == 0:
        new_ut = UserTimetable(name="Rozvrh", user_id=current_user.id)
        db.session.add(new_ut)
        db.session.commit()
        timetable_to_show_id = new_ut.id_
    else:
        # id of last added timetable:
        timetable_to_show_id = current_user.timetables.order_by(UserTimetable.id_)[-1].id_
    return jsonify({'next_url': url_for("timetable.user_timetable", id_=timetable_to_show_id)})



@login_required
@timetable.route("/moj-rozvrh/<id_>/rename", methods=['PATCH'])
def rename_timetable(id_):
    new_name = request.form['new_name']
    new_name = getUniqueName(new_name)
    ut = UserTimetable.query.get_or_404(id_)
    ut.name = new_name
    db.session.commit()

    # render new parts of the webpage:
    tabs_html = render_template("timetable/tabs.html", user_timetables=current_user.timetables, selected_timetable_key=ut.id_, title=ut.name)
    web_header_html = f"<h1>{ut.name}</h1>"
    title_html = render_template('title.html', title=ut.name)

    return jsonify({'tabs_html': tabs_html,
                    'web_header_html': web_header_html,
                    'title': ut.name,
                    'title_html': title_html})