from flask import render_template, Blueprint, request

from timetable.forms import ShowRoomsForm
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
def timetable_room(room_name):
    """Zobrazi rozvrh pre danu miestnost:"""
    web_header = "Rozvrh miestnosti " + room_name
    room = Room.query.filter_by(name=room_name).first()
    lessons = room.lessons.order_by(Lesson.day, Lesson.start)

    timetable = Timetable.Timetable(lessons)
    starting_times = timetable.get_starting_times()

    # panel_forms = timetable.get_panel_forms_dict()
    panel_forms = {}
    panel_forms['rooms'] = ShowRoomsForm()

    search_results = None
    if request.method == 'POST':
        # TODO: Switch - pre kazdy pripad panel form
        string = panel_forms['rooms'].show_rooms.data
        if string != '':
            #query DB:
            search_results = Room.query.filter(Room.name.contains(string)).all()

    return render_template('timetable/timetable.html', room_name=room_name, lessons_list=lessons, title=room_name, web_header=web_header,
                           timetable=timetable, starting_times=starting_times, panel_forms=panel_forms, search_results=search_results)
