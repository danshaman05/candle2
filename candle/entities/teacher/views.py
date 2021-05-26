from flask import Blueprint, render_template
from flask_login import current_user

from typing import Dict
from candle.models import Lesson, Teacher
from candle.timetable import timetable
from candle.helpers import get_ordered_dict, string_starts_with_ch
import unidecode


teacher = Blueprint('teacher', __name__)


@teacher.route('/ucitelia')
def list_teachers():
    """Show all teachers in the list."""
    teachers_list = Teacher.query.order_by(Teacher.family_name).all()
    teachers_dict = get_teachers_sorted_by_family_name(teachers_list)
    title = "Rozvrhy učiteľov"
    return render_template('teacher/list_teachers.html', teachers_dict=teachers_dict, title=title,
                           web_header=title)


@teacher.route('/ucitelia/<teacher_slug>', methods=['GET', 'POST'])
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
    """
    Vrati dictionary ucitelov zotriedenych podla zaciatocneho pismena v priezvisku.
    vstup: zoznam objektov triedy models.Teacher zoradenych podla priezviska (family_name)
    vystup: dictionary { string, List objektov Teacher}, kde klucom je zac. pismeno priezviska
    a hodnoty su objekty triedy Teacher
    """
    d = {}
    others = []    # specialna kategoria
    for teacher in teachers:
        if teacher.family_name is None or teacher.family_name == '':
            continue

        first_letter = (teacher.family_name[0])     # ziskame prve pismeno family_name (priezviska)
        if first_letter.isalpha() == False:    # niektore mena mozu zacinat na '.', alebo '/', (a pod.), tieto osetrime samostatne v kategorii Ostatne
            others.append(teacher)
            continue
        first_letter = unidecode.unidecode(first_letter)    # zmenime ho na pismeno bez diakritiky (napr. Č zmeni na C)
        if string_starts_with_ch(teacher.family_name):     # family_name zacinajuce na CH je samostatna kategoria.
            first_letter = 'Ch'
        if first_letter not in d:
            d[first_letter] = []
        d[first_letter].append(teacher)
    d['Ostatné'] = others

    return get_ordered_dict(d)