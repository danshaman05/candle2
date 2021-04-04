from flask import render_template, Blueprint, request
from flask_login import current_user

from ..helpers import get_ordered_dict
from ..models import Room, Lesson
from ..timetable import timetable
from typing import Dict


rooms = Blueprint('rooms', __name__)


@rooms.route('/miestnosti')
def list_rooms():
    """Show all rooms."""
    rooms_list = Room.query.order_by(Room.name).all()
    rooms_dict = get_rooms_sorted_by_dashes(rooms_list)  # rooms are in the dictionary sorted by prefix
    return render_template('rooms/list_rooms.html', rooms_dict=rooms_dict, title="Rozvrhy miestností")


@rooms.route('/miestnosti/<room_name>', methods=['GET', 'POST'])
def show_timetable(room_name):
    """Show a timetable for a room."""
    web_header = "Rozvrh miestnosti " + room_name
    room = Room.query.filter_by(name=room_name).first()
    lessons = room.lessons.order_by(Lesson.day, Lesson.start).all()
    t = timetable.Timetable(lessons)
    if current_user.is_authenticated:
        user_timetables = current_user.timetables
    else:
        user_timetables = None
    return render_template('timetable/timetable.html', room_name=room_name, title=room_name,
                           web_header=web_header, timetable=t,
                           user_timetables=user_timetables, infobox=False)


def get_rooms_sorted_by_dashes(rooms_lst) -> Dict:
    """
    Return OrderedDict that contains room names sorted by categories.

    The key in the OrderedDict is always the room prefix and the values are the given suffixes
    stored in the rooms_lst (E.g 'F1-108' has prefix 'F1' and suffix '108').

    :parameter rooms_lst: The list of the Room model objects.
    :return dictionary of str: List[str]
    """
    d = {}
    for room in rooms_lst:
        name = room.name
        if name == " ":   # we have one room with name " "
            continue

        dash_position = name.find('-')
        if dash_position == -1:  # name doesn't contain '-'
            prefix = suffix = name
        else:
            prefix = name[0 : dash_position]
            suffix = name[dash_position + 1 : ]

        # if the data are in bad format:
        # raise Exception("Bad data format for room. Room must be in format 'prefix-suffix', for example: 'F1-208'")

        #xMieRez is a special case:
        if 'xMieRez' in prefix:
            suffix = prefix
            prefix = "Ostatné"
            if prefix not in d:
                d[prefix] = []
            d[prefix].append(suffix)
        else:
            if prefix not in d:
                d[prefix] = []
            if prefix == suffix:
                d[prefix].append(suffix)
            else:
                d[prefix].append('-'.join([prefix, suffix]))
    return get_ordered_dict(d)

