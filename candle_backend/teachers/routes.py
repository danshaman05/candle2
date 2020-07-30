from flask import Blueprint, render_template

from ..helpers import get_teachers_sorted_by_family_name
from ..models import Lesson, Teacher
from .. import Timetable

from .. import temporary_path   # TODO presunut do config filu

teachers = Blueprint('teachers', __name__)

# Vypise vsetkych ucitelov (zoznam)
@teachers.route(temporary_path + '/ucitelia')
def list_teachers():
    """Vypise zoznam vsetkych ucitelov"""
    teachers_list = Teacher.query.order_by(Teacher.family_name).all()
    teachers_dict = get_teachers_sorted_by_family_name(teachers_list)

    return render_template('list_teachers.html', teachers_dict=teachers_dict)

@teachers.route(temporary_path + '/ucitelia/<teacher_slug>')
def timetable_teacher(teacher_slug):
    """ Zobrazi rozvrh daneho ucitela."""
    teacher = Teacher.query.filter_by(slug=teacher_slug).first()
    teacher_name = teacher.given_name + " " + teacher.family_name
    lessons = teacher.lessons.order_by(Lesson.day, Lesson.start).all()

    timetable = Timetable.Timetable(lessons)
    starting_times = timetable.get_starting_times()

    return render_template('timetable.html', teacher_name=teacher_name, lessons_list=lessons, title=teacher_name, web_header=teacher_name,
                           timetable=timetable, starting_times=starting_times)

