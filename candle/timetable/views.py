from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user, login_required
from sqlalchemy import or_

from ..models import UserTimetable, Lesson, Teacher
from ..timetable.Timetable import Timetable

timetable = Blueprint('timetable', __name__)


@timetable.route('/moj-rozvrh/<id_>', methods=['GET'])
@login_required
def user_timetable(id_):
    id_ = int(id_)
    user_timetables = current_user.timetables
    ut = UserTimetable.query.get(id_)
    lessons = ut.lessons.order_by(Lesson.day, Lesson.start).all()
    t = Timetable(lessons)
    if timetable is None:
        raise Exception("timetable cannot be None")

    # zobrazi rozvrh:
    return render_template('timetable/timetable.html',
                           title=ut.name, web_header=ut.name,
                           timetable=t,
                           user_timetables=user_timetables, selected_timetable_key=id_)


@timetable.route('/', methods=['GET', 'POST'])
def home():
    """
    ak je prihlaseny:
        ak ma nejake rozvrhy:
            zobrazi rozvrh daneho usera - vyberie najnovsi (podla id)
        inak:
            vytvori prazdny rozvrh a priradi ho uzivatelovi
    ak je odhlaseny:
        vypise INFOBOX
    """
    # je prihlaseny:
    if current_user.is_authenticated:
        # vyberieme jeden z userovych rozvrhov
        user_timetable = current_user.timetables.order_by(UserTimetable.id_)[-1]
        timetable = Timetable(user_timetable.lessons)
        if timetable is None:
            raise Exception("timetable cannot be None")

        # zobrazi rozvrh:
        return render_template('timetable/timetable.html',
                               title=user_timetable.name, web_header=user_timetable.name,
                               timetable=timetable,
                               user_timetables=current_user.timetables,
                               selected_timetable_key=user_timetable.id_,
                               infobox=False)
    else:  # je odhlaseny
        return render_template('timetable/timetable.html',
                               title='Rozvrh',

                               infobox=True)



# def check_forms():  # TODO poriesit cez JQUERY!
#     """skontroluje, ci bolo stlacene nejake tlacidlo z panela.
#     Ak ano, tak spracuje danu poziadavku a nastavi vysledok v paneli. """
#
#     if self.__button_clicked('rooms'):
#         search = self.__rooms_form.show_rooms.data
#         if search != '':  # TODO treba validovat string?
#             search = search.replace(" ", "%")
#             search = "%{}%".format(search)
#             rooms_list = Room.query.filter(Room.name.like(search)).all()  # TODO pouzit ilike?
#             self.set_results(rooms_list, 'rooms')
#
#     elif self.__button_clicked('teachers'):
#         search = self.__teachers_form.show_teachers.data
#         if search != '':
#             search = search.replace(" ", "%")
#             search = search.replace(".", "%")
#             search = "%{}%".format(search)
#
#             teachers = Teacher.query.filter(
#                 or_(Teacher.fullname.like(search),
#                     Teacher.fullname_reversed.like(search))) \
#                 .order_by(Teacher.family_name) \
#                 .limit(50).all()
#
#             self.set_results(list(teachers), 'teachers')
#
#     elif self.__button_clicked('student_groups'):
#         search = self.__student_groups_form.show_student_groups.data
#         if search != '':
#             search = search.replace(" ", "%")
#             search = "%{}%".format(search)
#             groups_list = StudentGroup.query.filter(StudentGroup.name.ilike(search)).all()
#             self.set_results(groups_list, 'student_groups')