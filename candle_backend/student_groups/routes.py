from flask import render_template, Blueprint

from ..helpers import get_student_groups_sorted_by_first_letter
from ..models import StudentGroup, Lesson

from .. import temporary_path   # TODO presunut do config filu

student_groups = Blueprint('student_groups', __name__)



@student_groups.route(temporary_path + '/kruzky')
def list_student_groups():
    groups_list = StudentGroup.query.all()
    student_groups_dict = get_student_groups_sorted_by_first_letter(groups_list)

    return render_template('list_student_groups.html', student_groups_dict=student_groups_dict)


@student_groups.route(temporary_path + '/kruzky/<student_group_name>')
def timetable_student_group(student_group_name):
    """ Zobrazi rozvrh pre dany kruzok."""
    web_header = "Rozvrh krúžku " + student_group_name
    group = StudentGroup.query.filter_by(name=student_group_name).first()

    lessons = group.lessons.order_by(Lesson.day, Lesson.start).all()


    return render_template('timetable.html', student_group_name=student_group_name, lessons_list=lessons,
                           web_header=web_header)
