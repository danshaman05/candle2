from flask import render_template, Blueprint
from ..models import Room, Lesson
from .. import Timetable
from ..helpers import get_rooms_sorted_by_dashes

from .. import temporary_path   # TODO presunut do config filu

rooms = Blueprint('rooms', __name__)    # Blueprint instancia


@rooms.route(temporary_path + '/miestnosti')
def list_rooms():
    # Vypise vsetky miestnosti (zoznam)
    rooms = Room.query.order_by(Room.name).all()
    rooms_dict = get_rooms_sorted_by_dashes(rooms)  # ucebne su v jednom dictionary rozdelene podla prefixu

    return render_template('list_rooms.html', rooms_dict=rooms_dict)


@rooms.route(temporary_path + '/miestnosti/<room_name>')
def timetable_room(room_name):
    # Zobrazi rozvrh pre danu miestnost:
    web_header = "Rozvrh miestnosti " + room_name
    room = Room.query.filter_by(name=room_name).first()
    lessons = room.lessons.order_by(Lesson.day, Lesson.start)

    layout = Timetable.Timetable(lessons)


    # Z lessons_list urobime graficky rozvrh (3d pole):
    #timetable = get_timetable(lessons_list)

    # print(len(timetable[1][0]) == 6)


    # TOTO TREBA PRESUNUT K TIMETABLE class, aby sme do template posunuli uz len objekt timetable
    # spocitame pocty stlpcov v timetable pre dane dni
    # column_counts = []
    # for columns_list in timetable:
    #     column_counts.append(len(columns_list))


    return render_template('timetable.html', room_name=room_name, lessons_list=lessons, title=room_name, web_header=web_header, layout=layout)

