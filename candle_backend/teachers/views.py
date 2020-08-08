from flask import Blueprint, render_template, request

from timetable.Panel import Panel
from ..helpers import get_teachers_sorted_by_family_name
from ..models import Lesson, Teacher
from timetable import Timetable

from .. import temporary_path  # TODO presunut do config filu

teachers = Blueprint('teachers', __name__)


# Vypise vsetkych ucitelov (zoznam)
@teachers.route(temporary_path + '/ucitelia')
def list_teachers():
    """Vypise zoznam vsetkych ucitelov"""
    teachers_list = Teacher.query.order_by(Teacher.family_name).all()
    teachers_dict = get_teachers_sorted_by_family_name(teachers_list)

    return render_template('teachers/list_teachers.html', teachers_dict=teachers_dict)


@teachers.route(temporary_path + '/ucitelia/<teacher_slug>', methods=['GET', 'POST'])
def timetable(teacher_slug):
    """ Zobrazi rozvrh daneho ucitela."""
    teacher = Teacher.query.filter_by(slug=teacher_slug).first()
    teacher_name = teacher.given_name + " " + teacher.family_name
    lessons = teacher.lessons.order_by(Lesson.day, Lesson.start).all()

    t = Timetable.Timetable(lessons)
    p = Panel()
    if request.method == 'POST':
        p.check_forms()

    return render_template('timetable/timetable.html', teacher_name=teacher_name, title=teacher_name,
                           web_header=teacher_name,
                           timetable=t, panel=p)
