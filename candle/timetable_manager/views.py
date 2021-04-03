from typing import List

from flask import Blueprint, request, url_for, jsonify, render_template
from flask_login import current_user, login_required
from .. import db
from ..models import UserTimetable, Teacher, Room, StudentGroup
import re

timetable_manager = Blueprint('editable_timetable_manager', __name__)


@timetable_manager.route("/new_timetable", methods=['POST'])
# @login_required
def new_timetable():
    # TODO docstring
    name = request.form['name']
    name = getUniqueName(name)
    ut = UserTimetable(name=name, user_id=current_user.id)
    db.session.add(ut)
    db.session.commit()
    return url_for("timetable.user_timetable", id_=ut.id_)


@timetable_manager.route("/delete_timetable", methods=['POST'])
@login_required
def delete_timetable():
    # TODO docstring
    rozvrh_url = request.form['url']
    id_ = int(rozvrh_url.split('/')[-1])  # id ziskame z URL
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
@login_required
def duplicate_timetable():
    timetable_url = request.form['data']
    """Examples of URL:
     /ucitelia/Stanislav-Antalic
     /miestnosti/B1-302
     /kruzky/1mFAA
     /moj-rozvrh/751
    """
    url_list = timetable_url.split('/')
    if "ucitelia" in url_list:
        i = url_list.index("ucitelia")
        slug = url_list[i + 1]  # pozicia ucitelovho slugu v url
        old_timetable = Teacher.query.filter_by(slug=slug).first_or_404()  # podla slugu najdeme ucitela
        new_name = getUniqueName(old_timetable.short_name)
        new_t = UserTimetable(name=new_name, user_id=current_user.id)

    elif "miestnosti" in url_list:
        i = url_list.index("miestnosti")
        name = url_list[i + 1]
        old_timetable = Room.query.filter_by(name=name).first_or_404()
        new_name = getUniqueName(old_timetable.name)
        new_t = UserTimetable(name=new_name, user_id=current_user.id)

    elif "kruzky" in url_list:
        i = url_list.index("kruzky")
        name = url_list[i + 1]
        old_timetable = StudentGroup.query.filter_by(name=name).first_or_404()
        new_name = getUniqueName(old_timetable.name)
        new_t = UserTimetable(name=new_name, user_id=current_user.id)

    elif "moj-rozvrh" in url_list:
        i = url_list.index("moj-rozvrh")
        id_ = url_list[i + 1]
        old_timetable = UserTimetable.query.get(id_)
        new_name = getUniqueName(old_timetable.name)
        new_t = UserTimetable(name=new_name, user_id=current_user.id)
    else:
        raise Exception("BAD URL format!")  # TODO nahradit Error page!

    db.session.add(new_t)
    for lesson in old_timetable.lessons:
        new_t.lessons.append(lesson)
    db.session.commit()
    return jsonify({'next_url': url_for("timetable.user_timetable", id_=new_t.id_)})


@timetable_manager.route("/rename_timetable", methods=['POST'])
@login_required
def rename_timetable():
    rozvrh_url = request.form['url']
    new_name = request.form['new_name']
    new_name = getUniqueName(new_name)
    id_ = int(rozvrh_url.split('/')[-1])  # id ziskame z URL
    ut = UserTimetable.query.get(id_)
    ut.name = new_name
    db.session.commit()

    tabs_html = render_template("timetable/tabs.html", user_timetables=current_user.timetables, selected_timetable_key=ut.id_, title=ut.name)
    web_header_html = f"<h1>{ut.name}</h1>"
    title_html = render_template('title.html', title=ut.name)

    return jsonify({'tabs_html': tabs_html,
                    'web_header_html': web_header_html,
                    'title': ut.name,
                    'title_html': title_html})


def getUniqueName(name) -> str:
    """ This method ensures that this timetable will not have the same name as some other one.
    :param name: meno pre novy rozvrh
    :return: nove unikatne meno pre rozvrh
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

    # try if "name + (index)" is unique:
    index = 2
    while True:
        new_name = f"{name} ({index})"
        if new_name not in timetables_names:
            return new_name
        index += 1
