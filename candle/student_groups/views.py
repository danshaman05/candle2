from typing import Dict
from flask import render_template, Blueprint
from flask_login import current_user

from candle.models import StudentGroup, Lesson
from candle.timetable import timetable

student_groups = Blueprint('student_groups', __name__)



@student_groups.route('/kruzky')
def list_student_groups():
    """Show all student groups."""
    groups_list = StudentGroup.query.order_by(StudentGroup.name).all()
    student_groups_dict = get_student_groups_sorted_by_first_letter(groups_list)

    return render_template('student_groups/list_student_groups.html',
                           student_groups_dict=student_groups_dict,
                           title="Rozvrhy krúžkov")


@student_groups.route('/kruzky/<group_url_id>', methods=['GET'])
def show_timetable(group_url_id: str):
    """Show a timetable for a student-group."""

    if group_url_id.isnumeric():
        student_group = StudentGroup.query.filter_by(id_=group_url_id).first_or_404()
    else:
        student_group = StudentGroup.query.filter_by(name=group_url_id).first_or_404()
    web_header = "Rozvrh krúžku " + student_group.name
    lessons = student_group.lessons.order_by(Lesson.day, Lesson.start).all()
    t = timetable.Timetable(lessons)

    if current_user.is_authenticated:
        user_timetables = current_user.timetables
    else:
        user_timetables = None
    return render_template('timetable/timetable.html', title=student_group.name,
                           student_group_name=student_group.name,
                           web_header=web_header, timetable=t,
                           user_timetables=user_timetables, show_welcome=False)


def get_student_groups_sorted_by_first_letter(student_groups) -> Dict:
    """Return student-groups in a dictionary sorted by the first letter."""
    result_dict = {}
    for group in student_groups:
        first_letter = group.name[0]
        if first_letter not in result_dict:
            result_dict[first_letter] = []
        result_dict[first_letter].append(group)
    return result_dict
