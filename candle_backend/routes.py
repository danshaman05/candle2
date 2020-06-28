from typing import List, Dict

from flask import render_template
from candle_backend.models import Room, Lesson, LessonType, Subject, Teacher, StudentGroup
from candle_backend import app
from candle_backend.helpers import get_rooms_sorted_by_dashes, get_teachers_sorted_by_family_name, get_student_groups_sorted_by_first_letter, minutes_2_time, get_short_name


@app.route('/')
def home(): # TODO
    return '<a href="/miestnosti">Rozvrhy všetkých miestností</a>' \
           '<br><a href="/ucitelia">Rozvrhy všetkých učiteľov</a>' \
           '<br><a href="/kruzky">Rozvrhy všetkých krúžkov</a>'


def get_lessons(lessons_objects) -> List:
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
                teacher_short = get_short_name(teacher.given_name, teacher.family_name)
                teachers_dict[teacher.slug] = teacher_short

        lesson_dict['teachers_dict'] = teachers_dict
        lesson_dict['day'] = lo.get_day_abbreviation()
        lesson_dict['start'] = minutes_2_time(lo.start)
        lesson_dict['end'] = minutes_2_time(lo.end)
        lesson_dict['room'] = lo.room.name
        lesson_dict['type'] = LessonType.query.get(lo.lesson_type_id).name
        lesson_dict['code'] = subject.short_code
        lesson_dict['subject'] = subject.name
        lesson_dict['note'] = lo.note if lo.note is not None else ''

        lessons_list.append(lesson_dict)
    return lessons_list


#### MODUL ROOM ####

@app.route('/miestnosti')
def list_rooms():
    # Vypise vsetky miestnosti (zoznam)
    rooms = Room.query.order_by(Room.name).all()
    rooms_dict = get_rooms_sorted_by_dashes(rooms)  # ucebne su v jednom dictionary rozdelene podla prefixu

    return render_template('list_rooms.html', rooms_dict=rooms_dict)


@app.route('/miestnosti/<room_name>')
def timetable_room(room_name):
    # Zobrazi rozvrh pre danu miestnost:
    room = Room.query.filter_by(name=room_name).first()
    lessons_objects = room.lessons.order_by(Lesson.day, Lesson.start)
    lessons_list = get_lessons(lessons_objects)
    web_header = "Rozvrh miestnosti " + room_name
    return render_template('timetable.html', room_name=room_name, lessons=lessons_list, title=room_name, web_header=web_header)



#### MODUL TEACHER ####

# Vypise vsetkych ucitelov (zoznam)
@app.route('/ucitelia')
def list_teachers():
    teachers = Teacher.query.order_by(Teacher.family_name)
    teachers_dict = get_teachers_sorted_by_family_name(teachers)

    return render_template('list_teachers.html', teachers_dict=teachers_dict)


@app.route('/ucitelia/<teacher_slug>')
def timetable_teacher(teacher_slug):
    ''' Zobrazi rozvrh daneho ucitela.'''
    teacher = Teacher.query.filter_by(slug=teacher_slug).first()
    teacher_name = teacher.given_name + " " + teacher.family_name

    lessons_objects = teacher.lessons.order_by(Lesson.day, Lesson.start).all()
    lessons_list = get_lessons(lessons_objects)

    return render_template('timetable.html', teacher_name=teacher_name, lessons=lessons_list, title=teacher_name, web_header=teacher_name)





#### MODUL KRUZKY ####

@app.route('/kruzky')
def list_student_groups():
    student_groups = StudentGroup.query.all()
    student_groups_dict = get_student_groups_sorted_by_first_letter(student_groups)

    return render_template('list_student_groups.html', student_groups_dict=student_groups_dict)



@app.route('/kruzky/<student_group_name>')
def timetable_student_group(student_group_name):
    ''' Zobrazi rozvrh pre dany kruzok.'''
    group = StudentGroup.query.filter_by(name=student_group_name).first()

    lessons_objects = group.lessons.order_by(Lesson.day, Lesson.start).all()
    lessons_list = get_lessons(lessons_objects)
    web_header = "Rozvrh krúžku " + student_group_name

    return render_template('timetable.html', student_group_name=student_group_name, lessons=lessons_list,
                           web_header=web_header)