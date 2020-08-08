from flask import render_template, Blueprint, request

from timetable.Panel import Panel
from ..models import Room, Lesson
from timetable import Timetable
from ..helpers import get_rooms_sorted_by_dashes

from .. import temporary_path   # TODO presunut do config filu

rooms = Blueprint('rooms', __name__)    # Blueprint instancia


@rooms.route(temporary_path + '/miestnosti')
def list_rooms():
    """Vypise vsetky miestnosti (zoznam)"""
    rooms_list = Room.query.order_by(Room.name).all()
    rooms_dict = get_rooms_sorted_by_dashes(rooms_list)  # ucebne su v jednom dictionary rozdelene podla prefixu

    return render_template('rooms/list_rooms.html', rooms_dict=rooms_dict)


@rooms.route(temporary_path + '/miestnosti/<room_name>', methods=['GET', 'POST'])
def timetable(room_name):
    """Zobrazi rozvrh pre danu miestnost:"""
    web_header = "Rozvrh miestnosti " + room_name
    room = Room.query.filter_by(name=room_name).first()
    lessons = room.lessons.order_by(Lesson.day, Lesson.start)

    t = Timetable.Timetable(lessons)
    p = Panel()

    if request.method == 'POST':
        # skontroluje, ci bolo stlacene nejake tlacidlo z panela. Ak ano, tak spracuje danu poziadavku a nastavi vysledok v paneli.
        p.check_forms()

    return render_template('timetable/timetable.html', room_name=room_name, title=room_name, web_header=web_header,
                           timetable=t, panel=p)
