from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

from ..models import UserTimetable
from timetable.Panel import Panel
from timetable.Timetable import Timetable

timetable = Blueprint('timetable', __name__)  # Blueprint instancia


@timetable.route('/moj/rozvrh/<id_>', methods=['GET'])
@login_required
def user_timetable(id_):
    id_ = int(id_)

    user_timetables = current_user.timetables
    ut = UserTimetable.query.get(id_)
    gt = Timetable(ut.lessons)  # TODO premennu gt zmenit na timetable?
    if gt is None:
        raise Exception("timetable cannot be None")

    # zobrazi rozvrh:
    panel = Panel()
    if request.method == 'POST':
        panel.check_forms()
    return render_template('timetable/timetable.html',
                           title=ut.name, web_header=ut.name,
                           timetable=gt, panel=panel,
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
        # nacitame userove rozvrhy:

        # vyberieme jeden z userovych rozvrhov
        user_timetable = current_user.timetables.order_by(UserTimetable.id_)[-1]
        gt = Timetable(user_timetable.lessons)
        if gt is None:
            raise Exception("timetable cannot be None")

        # zobrazi rozvrh:
        panel = Panel()
        if request.method == 'POST':        # TODO poriesit cez JQUERY
            panel.check_forms()
        return render_template('timetable/timetable.html',
                               title=user_timetable.name, web_header=user_timetable.name,
                               timetable=gt, panel=panel,
                               user_timetables=current_user.timetables,
                               selected_timetable_key=user_timetable.id_,
                               infobox=False)

    else:  # je odhlaseny
        panel = Panel()
        if request.method == 'POST':
            panel.check_forms()
        return render_template('timetable/timetable.html',
                               title='Rozvrh',
                               # web_header='Rozvrh',
                               # timetable=None,  # TODO nech ani nedava parameter
                               panel=panel,
                               infobox=True)
