from flask import render_template, Blueprint, request
from flask_login import current_user

from helpers import get_ordered_dict
from ..models import Room, Lesson
from timetable import Timetable
from typing import Dict


rooms = Blueprint('rooms', __name__)    # Blueprint instancia


@rooms.route('/miestnosti')
def list_rooms():
    """Vypise vsetky miestnosti (zoznam)"""
    rooms_list = Room.query.order_by(Room.name).all()
    rooms_dict = get_rooms_sorted_by_dashes(rooms_list)  # ucebne su v jednom dictionary rozdelene podla prefixu

    return render_template('rooms/list_rooms.html', rooms_dict=rooms_dict, title="Rozvrhy miestností")


@rooms.route('/miestnosti/<room_name>', methods=['GET', 'POST'])
def timetable(room_name):
    """Zobrazi rozvrh pre danu miestnost:"""
    web_header = "Rozvrh miestnosti " + room_name
    room = Room.query.filter_by(name=room_name).first()
    lessons = room.lessons.order_by(Lesson.day, Lesson.start).all()

    t = Timetable.Timetable(lessons)
    p = Panel()

    if current_user.is_authenticated:
        user_timetables = current_user.timetables
    else:
        user_timetables = None


    return render_template('timetable/timetable.html', room_name=room_name, title=room_name,
                           web_header=web_header, timetable=t, panel=p,
                           user_timetables=user_timetables, infobox=False)


def get_rooms_sorted_by_dashes(rooms_lst) -> Dict:
    '''
    Rozdeli mena miestnosti podla kategorii do dictionary, kde key je vzdy prefix miestnosti a value su
    dane sufixy ulozene v poli. (napr. F1-108 ma prefix F1 a sufix 108)
    vstup: zoznam objektov triedy models.Room
    vystup: dictionary {string, List stringov}
    '''
    d = {}
    for room in rooms_lst:
        name = room.name
        if name == " ":   # v tabulke room mame jednu miestnost s name " "
            continue

        dash_position = name.find('-')
        if (dash_position) == -1:  # name neobsahuje '-'
            prefix = suffix = name
        else:
            prefix = name[0 : dash_position]
            suffix = name[dash_position + 1 : ]

        # ak su data v zlom formate:
        # raise Exception("Bad data format for room. Room must be in format 'prefix-suffix', for example: 'F1-208'")

        #xMieRez je specialny pripad:
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

