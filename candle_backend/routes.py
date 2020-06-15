from typing import List, Dict

from flask import render_template
from candle_backend.models import Room, Lesson, LessonType, Subject, Teacher
from candle_backend import app
from candle_backend.helpers import getRoomsSortedByDashes_dict, getTeachersSortedByLastname_dict, minutes2time, shortName


@app.route('/')
def home(): # TODO
    return '<a href="/miestnosti">Rozvrhy všetkých miestností</a>' \
           '<br><a href="/ucitelia">Rozvrhy všetkých učiteľov</a>'

#### MODUL ROOM ####

@app.route('/miestnosti')
def list_rooms():
    # Vypise vsetky miestnosti (zoznam)
    rooms = Room.query.all()
    rooms_dict = getRoomsSortedByDashes_dict(rooms)  # ucebne su v jednom dictionary rozdelene podla prefixu

    return render_template('show_all_rooms.html', rooms_dict=rooms_dict)


@app.route('/miestnosti/<room_name>')
def roomTimetable(room_name):
    # Zobrazi rozvrh pre danu miestnost:
    room = Room.query.filter_by(name=room_name).first()
    lessons_objects = room.lessons.order_by(Lesson.day, Lesson.start)
    lessons_list = getLessons_list(lessons_objects)
    return render_template('timetable_room.html', room_name=room_name, lessons=lessons_list)




#### MODUL TEACHER ####

# Vypise vsetkych ucitelov (zoznam)
@app.route('/ucitelia')
def list_teachers():
    teachers = Teacher.query.order_by(Teacher.family_name)
    teachers_dict = getTeachersSortedByLastname_dict(teachers)  # ucebne su v jednom dictionary rozdelene podla prefixu

    return render_template('show_all_teachers.html', teachers_dict=teachers_dict)


@app.route('/ucitelia/<teacher_slug>')
def teacherTimetable(teacher_slug):
    ''' Zobrazi rozvrh daneho ucitela.'''
    teacher = Teacher.query.filter_by(slug=teacher_slug).first()
    teacher_name = teacher.given_name + " " + teacher.family_name

    lessons_objects = teacher.lessons.order_by(Lesson.day, Lesson.start).all()
    lessons_list = getLessons_list(lessons_objects)

    return render_template('timetable_teacher.html', teacher_name=teacher_name, lessons=lessons_list)


def getLessons_list(lessons_objects) -> List:
    lessons_list: List[Dict] = []
    for lo in lessons_objects:
        subject = lo.subject
        teachers = lo.teachers.all()

        lesson_dict: Dict[str, str] = {}
        teachers_dict: Dict[str, str] = {}  # Jednu lesson moze ucit viac ucitelov, preto si pre kazdu lesson vytvorime dict ucitelov

        if len(teachers) == 1 and teachers[0].given_name == '':     # napr. predmet "pisomky" ma takeho ucitela
            lesson_dict['teachers_dict'] = None
        else:
            for teacher in teachers:
                teacher_short = shortName(teacher.given_name, teacher.family_name)
                teachers_dict[teacher.slug] = teacher_short

        lesson_dict['teachers_dict'] = teachers_dict
        lesson_dict['day'] = lo.getDayAbbreviation()
        lesson_dict['start'] = minutes2time(lo.start)
        lesson_dict['end'] = minutes2time(lo.end)
        lesson_dict['room'] = lo.room.name
        lesson_dict['type'] = LessonType.query.get(lo.lesson_type_id)
        lesson_dict['code'] = subject.short_code
        lesson_dict['subject'] = subject.name
        lesson_dict['note'] = lo.note if lo.note is not None else ''

        lessons_list.append(lesson_dict)
    return lessons_list
