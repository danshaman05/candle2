from flask import Blueprint, render_template
from flask_login import current_user

from typing import Dict
from candle.models import Lesson, Teacher
from candle.timetable import timetable
from candle.entities.helpers import  string_starts_with_ch
import unidecode


teacher = Blueprint('teacher',
                    __name__,
                    template_folder='templates')


@teacher.route('/ucitelia')
def list_teachers():
    """Show all teachers in the list."""
    teachers_list = Teacher.query.order_by(Teacher.family_name).all()
    teachers_dict = get_teachers_sorted_by_family_name(teachers_list)
    title = "Rozvrhy učiteľov"
    return render_template('teacher/list_teachers.html', teachers_dict=teachers_dict, title=title,
                           web_header=title)


@teacher.route('/ucitelia/<teacher_slug>')
def show_timetable(teacher_slug):
    """Show a timetable for a teacher."""
    teacher = Teacher.query.filter(Teacher.slug==teacher_slug).first_or_404()
    teacher_name = teacher.given_name + " " + teacher.family_name
    lessons = teacher.lessons.order_by(Lesson.day, Lesson.start).all()
    t = timetable.Timetable(lessons)
    if current_user.is_authenticated:
        user_timetables = current_user.timetables
    else:
        user_timetables = None
    return render_template('timetable/timetable.html',
                           teacher_name=teacher_name, title=teacher_name,
                           web_header=teacher_name, timetable=t,
                           user_timetables=user_timetables, show_welcome=False)


def get_teachers_sorted_by_family_name(teachers) -> Dict:
    """Return a dictionary that contains teachers sorted by the first letter of the family_name.

    input: list of objects of model Teacher sorted by the family_name
    output: dictionary (string: List[Teacher]), where the key is the first letter of family_name
    and values are objects of model Teacher
    """
    d = {}
    others = []    # special category
    for teacher in teachers:
        if teacher.family_name is None or teacher.family_name == '':
            continue

        first_letter = (teacher.family_name[0])
        if first_letter.isalpha() == False:    # some names starts with dot '.', or forwardslash '/', (etc.)
            others.append(teacher)
            continue
        first_letter = unidecode.unidecode(first_letter)    # get rid of diacritics  (Č change to C)
        if string_starts_with_ch(teacher.family_name):     # family_name that starts on a "CH" is a special category
            first_letter = 'Ch'
        if first_letter not in d:
            d[first_letter] = []
        d[first_letter].append(teacher)
    d['Ostatné'] = others

    return d