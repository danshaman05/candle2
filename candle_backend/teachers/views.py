from flask import Blueprint, render_template, request
from flask_login import current_user

from timetable.Panel import Panel
from typing import Dict
from ..models import Lesson, Teacher
from timetable import Timetable
from helpers import get_ordered_dict, string_starts_with_ch
import unidecode


teachers = Blueprint('teachers', __name__)


# Vypise vsetkych ucitelov (zoznam)
@teachers.route('/ucitelia')
def list_teachers():
    """Vypise zoznam vsetkych ucitelov"""
    teachers_list = Teacher.query.order_by(Teacher.family_name).all()
    teachers_dict = get_teachers_sorted_by_family_name(teachers_list)
    return render_template('teachers/list_teachers.html', teachers_dict=teachers_dict, title="Rozvrhy učiteľov")


@teachers.route('/ucitelia/<teacher_slug>', methods=['GET', 'POST'])
def timetable(teacher_slug):
    """ Zobrazi rozvrh daneho ucitela."""
    teacher = Teacher.query.filter_by(slug=teacher_slug).first()
    teacher_name = teacher.given_name + " " + teacher.family_name
    lessons = teacher.lessons.order_by(Lesson.day, Lesson.start).all()

    t = Timetable.Timetable(lessons)
    panel = Panel()
    if request.method == 'POST':
        panel.check_forms()

    if current_user.is_authenticated:
        user_timetables = current_user.timetables
    else:
        user_timetables = None

    return render_template('timetable/timetable.html',
                           teacher_name=teacher_name, title=teacher_name,
                           web_header=teacher_name, timetable=t,
                           panel=panel, user_timetables=user_timetables, infobox=False)


def get_teachers_sorted_by_family_name(teachers) -> Dict:
    ''' Vrati dictionary ucitelov zotriedenych podla zaciatocneho pismena v priezvisku.
    vstup: zoznam objektov triedy models.Teacher zoradenych podla priezviska (family_name)
    vystup: dictionary { string, List objektov Teacher}, kde klucom je zac. pismeno priezviska
    a hodnoty su objekty triedy Teacher'''

    d = {}
    ostatne = []    # specialna kategoria
    for teacher in teachers:
        if teacher.family_name is None or teacher.family_name == '':
            continue

        first_letter = (teacher.family_name[0])     # ziskame prve pismeno family_name (priezviska)
        if first_letter.isalpha() == False:    # niektore mena mozu zacinat na '.', alebo '/', (a pod.), tieto osetrime samostatne v kategorii Ostatne
            ostatne.append(teacher)
            continue
        first_letter = unidecode.unidecode(first_letter)    # zmenime ho na pismeno bez diakritiky (napr. Č zmeni na C)

        if string_starts_with_ch(teacher.family_name):     # family_name zacinajuce na CH je samostatna kategoria.
            first_letter = 'Ch'

        if first_letter not in d:
            d[first_letter] = []
        d[first_letter].append(teacher)

    d['Ostatné'] = ostatne

    return get_ordered_dict(d)