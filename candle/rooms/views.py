from flask import render_template, Blueprint
from flask_login import current_user

from candle.helpers import get_ordered_dict
from candle.models import Room, Lesson, Subject
from candle.timetable import timetable
from typing import Dict


rooms = Blueprint('rooms', __name__)


@rooms.route('/miestnosti')
def list_rooms():
    """Show all rooms."""
    rooms_list = Room.query.order_by(Room.name).all()
    rooms_dict = get_rooms_sorted_by_dashes(rooms_list)  # rooms are in the dictionary sorted by prefix
    return render_template('rooms/list_rooms.html',
                           rooms_dict=rooms_dict,
                           title="Rozvrhy miestností")


@rooms.route('/miestnosti/<room_url_id>')
def show_timetable(room_url_id):
    """Show a timetable for a room."""
    room = Room.query.filter((Room.name == room_url_id) | (Room.id_==room_url_id)).first()
    lessons = room.lessons.join(Subject).order_by(Lesson.day, Lesson.start, Subject.name).all()


    t = timetable.Timetable(lessons)
    if current_user.is_authenticated:
        user_timetables = current_user.timetables
    else:
        user_timetables = None
    return render_template('timetable/timetable.html', room_name=room.name, title=room.name,
                           timetable=t, user_timetables=user_timetables, show_welcome=False)


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

    return get_ordered_dict(d)

