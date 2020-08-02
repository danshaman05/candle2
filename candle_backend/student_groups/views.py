from flask import render_template, Blueprint

from ..helpers import get_student_groups_sorted_by_first_letter
from ..models import StudentGroup, Lesson

from .. import temporary_path  # TODO presunut do config filu
from timetable import Timetable

student_groups = Blueprint('student_groups', __name__)



@student_groups.route(temporary_path + '/kruzky')
def list_student_groups():
    groups_list = StudentGroup.query.all()
    student_groups_dict = get_student_groups_sorted_by_first_letter(groups_list)

    return render_template('student_groups/list_student_groups.html', student_groups_dict=student_groups_dict)


@student_groups.route(temporary_path + '/kruzky/<student_group_name>', methods=['GET', 'POST'])
def timetable_student_group(student_group_name):
    """ Zobrazi rozvrh pre dany kruzok."""
    web_header = "Rozvrh krúžku " + student_group_name
    group = StudentGroup.query.filter_by(name=student_group_name).first()

    lessons = group.lessons.order_by(Lesson.day, Lesson.start).all()

    timetable = Timetable.Timetable(lessons)
    starting_times = timetable.get_starting_times()
    panel_forms = timetable.get_panel_forms_dict()

    return render_template('timetable/timetable.html', student_group_name=student_group_name, lessons_list=lessons,
                           web_header=web_header, timetable=timetable, starting_times=starting_times, panel_forms=panel_forms)
