from typing import List

from flask import render_template
from .models import Room, Lesson, Teacher, StudentGroup
from . import app, Timetable
from .helpers import get_rooms_sorted_by_dashes, get_teachers_sorted_by_family_name, get_student_groups_sorted_by_first_letter

temporary_path = '/2016-2017-zima'

@app.route(temporary_path + '/')
def home(): # TODO
    return f'<a href="{temporary_path}/miestnosti">Rozvrhy všetkých miestností</a>' \
           f'<br><a href="{temporary_path}/ucitelia">Rozvrhy všetkých učiteľov</a>' \
           f'<br><a href="{temporary_path}/kruzky">Rozvrhy všetkých krúžkov</a>'







#### MODUL ROOM ####

@app.route(temporary_path + '/miestnosti')
def list_rooms():
    # Vypise vsetky miestnosti (zoznam)
    rooms = Room.query.order_by(Room.name).all()
    rooms_dict = get_rooms_sorted_by_dashes(rooms)  # ucebne su v jednom dictionary rozdelene podla prefixu

    return render_template('list_rooms.html', rooms_dict=rooms_dict)


@app.route(temporary_path + '/miestnosti/<room_name>')
def timetable_room(room_name):
    # Zobrazi rozvrh pre danu miestnost:
    room = Room.query.filter_by(name=room_name).first()
    lessons_objects = room.lessons.order_by(Lesson.day, Lesson.start)

    timetable = Timetable.Timetable(lessons_objects)  ###


    # Z lessons_list urobime graficky rozvrh (3d pole):
    #timetable = get_timetable(lessons_list)
    # print(timetable)

    # print(len(timetable[1][0]) == 6)

    web_header = "Rozvrh miestnosti " + room_name
    #format_for_template(lessons_list)   # naformatuje niektore data v lessons_list pre vystup do template

    # TOTO TREBA PRESUNUT K TIMETABLE class, aby sme do template posunuli uz len objekt timetable
    # spocitame pocty stlpcov v timetable pre dane dni
    # column_counts = []
    # for columns_list in timetable:
    #     column_counts.append(len(columns_list))


    return render_template('timetable.html', room_name=room_name, lessons_list=lessons_objects, title=room_name, web_header=web_header, timetable=timetable)



#### MODUL TEACHER ####

# Vypise vsetkych ucitelov (zoznam)
@app.route(temporary_path + '/ucitelia')
def list_teachers():
    teachers = Teacher.query.order_by(Teacher.family_name).all()

    teachers_dict = get_teachers_sorted_by_family_name(teachers)

    return render_template('list_teachers.html', teachers_dict=teachers_dict)

@app.route(temporary_path + '/ucitelia/<teacher_slug>')
def timetable_teacher(teacher_slug):
    ''' Zobrazi rozvrh daneho ucitela.'''
    teacher = Teacher.query.filter_by(slug=teacher_slug).first()
    teacher_name = teacher.given_name + " " + teacher.family_name

    lessons_objects = teacher.lessons.order_by(Lesson.day, Lesson.start).all()
    lessons_list = get_lessons(lessons_objects)

    format_for_template(lessons_list)
    return render_template('timetable.html', teacher_name=teacher_name, lessons=lessons_list, title=teacher_name, web_header=teacher_name)




#### MODUL KRUZKY ####

@app.route(temporary_path + '/kruzky')
def list_student_groups():
    student_groups = StudentGroup.query.all()
    student_groups_dict = get_student_groups_sorted_by_first_letter(student_groups)

    return render_template('list_student_groups.html', student_groups_dict=student_groups_dict)


@app.route(temporary_path + '/kruzky/<student_group_name>')
def timetable_student_group(student_group_name):
    ''' Zobrazi rozvrh pre dany kruzok.'''
    group = StudentGroup.query.filter_by(name=student_group_name).first()

    lessons_objects = group.lessons.order_by(Lesson.day, Lesson.start).all()
    lessons_list = get_lessons(lessons_objects)
    web_header = "Rozvrh krúžku " + student_group_name

    format_for_template(lessons_list)
    return render_template('timetable.html', student_group_name=student_group_name, lessons=lessons_list,
                           web_header=web_header)
