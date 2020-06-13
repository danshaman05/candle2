from flask import render_template
from candle_backend.models import Room, Lesson, LessonType, Subject, Teacher, Teacher_lessons
from candle_backend import app
from candle_backend.helpers import getRoomsSortedByDashes_dict, getTeachersSortedByLastname_dict, minutes2time, shortName


@app.route('/')
def home(): # TODO
    return '<a href="/miestnosti">Rozvrhy všetkých miestností</a>' \
           '<br><a href="/ucitelia">Rozvrhy všetkých učiteľov</a>'

#### MODUL ROOM ####

# Vypise vsetky miestnosti (zoznam)
@app.route('/miestnosti')
def list_rooms():
    rooms = Room.query.all()
    rooms_dict = getRoomsSortedByDashes_dict(rooms)  # ucebne su v jednom dictionary rozdelene podla prefixu

    return render_template('show_all_rooms.html', rooms_dict=rooms_dict)


# zobrazi rozvrh pre danu miestnost:
@app.route('/miestnosti/<room_name>')
def roomTimetable(room_name):
    # nacitame z DB vsetky hodiny, kt. maju room == room_name
    room_id1 = Room.query.filter_by(name=room_name).first()
    lessons_objects = Lesson.query.filter_by(room_id=room_id1.id)\
        .order_by(Lesson.day, Lesson.start)

    lessons = []
    for lo in lessons_objects:
        subject = Subject.query.filter_by(id=lo.subject_id).first()
        query = Teacher_lessons.query.filter_by(lesson_id=lo.id)
        teacher_lessons_ids = [x.teacher_id for x in query.all()]  # chceme iba idcka ucitelov, kt. ucia dany predmet

        teachers = Teacher.query.filter(Teacher.id.in_(teacher_lessons_ids)).all()

        lesson = {}     # Kazda lesson bude dictionary.
        teachers_dict = {}      # Jednu lesson moze ucit viac ucitelov, preto si vytvorime dict ucitelov
        for teacher in teachers:
            teacher = Teacher.query.filter_by(id=teacher.id).first()
            teacher_short = shortName(teacher.given_name, teacher.family_name)
            teachers_dict[teacher.slug] = teacher_short

        lesson['teachers_dict'] = teachers_dict
        lesson['day'] = lo.getDayAbbreviation()
        lesson['start'] = minutes2time(lo.start)
        lesson['end'] = minutes2time(lo.end)
        lesson['room'] = room_name
        lesson['type'] = LessonType.query.filter_by(id=lo.lesson_type_id).first().name
        lesson['code'] = subject.short_code
        lesson['subject'] = subject.name
        lesson['note'] = lo.note if lo.note is not None else ''
        lessons.append(lesson)

    return render_template('timetable_room.html', room_name=room_name, lessons=lessons)



#### MODUL TEACHER ####

# Vypise vsetkych ucitelov (zoznam)
@app.route('/ucitelia')
def list_teachers():
    teachers = Teacher.query.order_by(Teacher.family_name).all()
    teachers_dict = getTeachersSortedByLastname_dict(teachers)  # ucebne su v jednom dictionary rozdelene podla prefixu

    return render_template('show_all_teachers.html', teachers_dict=teachers_dict)


@app.route('/ucitelia/<teacher_slug>')
def teacherTimetable(teacher_slug):
    '''Ziskame'''

    return ''   # TODO !!