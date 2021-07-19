from flask import render_template, Blueprint
from flask_login import current_user

from candle.models import Room, Lesson, Subject
from candle.timetable import layout
from typing import Dict


room = Blueprint('room',
                 __name__,
                 template_folder='templates')


@room.route('/miestnosti')
def list_rooms():
    """Show all rooms."""
    rooms_list = Room.query.order_by(Room.name).all()
    rooms_dict = get_rooms_sorted_by_dashes(rooms_list)  # rooms are in the dictionary sorted by prefix
    title = "Rozvrhy miestností"
    return render_template('room/list_rooms.html', rooms_dict=rooms_dict, title=title,
                           web_header=title)


@room.route('/miestnosti/<room_url_id>')
def show_timetable(room_url_id):
    """Show a timetable for a room."""
    if room_url_id.isnumeric():
        room = Room.query.filter_by(id_=room_url_id).first_or_404()
    else:
        room = Room.query.filter_by(name=room_url_id).first_or_404()
    web_header = "Rozvrh miestnosti " + room.name

    lessons = room.lessons.join(Subject).order_by(Lesson.day, Lesson.start, Subject.name).all()
    t = layout.Layout(lessons)
    if current_user.is_authenticated:
        my_timetables = current_user.timetables
    else:
        my_timetables = None
    return render_template('timetable/timetable.html', room_name=room.name, title=room.name,
                           timetable=t, my_timetables=my_timetables, show_welcome=False,
                           web_header=web_header)


def get_rooms_sorted_by_dashes(rooms_lst) -> Dict:
    """
    Return OrderedDict that contains rooms sorted by categories.

    The key in the OrderedDict is always the room prefix and the values are rooms (objects of model Room)
     (For example'F1-108' has prefix 'F1').

    :parameter rooms_lst: The list of the Room model objects.
    :return OrderedDict (dict of str: list), where key is the prefix and the value is a list of Rooms.
    """
    d = {}
    for room in rooms_lst:
        url_id = room.url_id
        if url_id == " ":   # we have one room with empty name (" ")
            continue
        prefix = room.prefix

        # insert data into dictionary:
        if prefix not in d:
            d[prefix] = []
        d[prefix].append(room)

    return d

