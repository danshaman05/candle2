from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

from ..models import UserTimetable
from timetable.Panel import Panel
from timetable.Timetable import Timetable

timetable = Blueprint('timetable', __name__)  # Blueprint instancia

@login_required
@timetable.route('/moj/rozvrh/<id_>', methods=['GET'])
def user_timetable(id_):
    id_ = int(id_)

    user_timetables = current_user.timetables
    ut = UserTimetable.query.get(id_)
    gt = Timetable(ut.lessons)    # TODO premennu gt zmenit na timetable?
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
            zobrazi rozvrh daneho usera - vyberie posledne aktualizovany   #TODO dorobit prepinanie rozvrhov
        inak:
            vytvori prazdny rozvrh a priradi ho uzivatelovi


    ak je neprihlaseny:
        (pracuje sa s anonym. navstevnikom)
        vytvori prazdny rozvrh ( vratane panelu so vsetkym) a zobrazi ho
        dany rozvrh si zapamata do session
    """
    # logout_user()

    # ak je prihlaseny:

    if current_user.is_authenticated:
        # nacitame userove rozvrhy:

        #vyberieme jeden z userovych rozvrhov
        ut = current_user.timetables.first()
        # ut = UserTimetable.query.filter_by(user_id=current_user.id_).first()        # TODO upravit na najnovsi - s najvyssim id ??
        gt = Timetable(ut.lessons)
        if gt is None:
            raise Exception("timetable cannot be None")

        # zobrazi rozvrh:
        panel = Panel()
        if request.method == 'POST':
            panel.check_forms()
        return render_template('timetable/timetable.html',
                               title=ut.name, web_header=ut.name,
                               timetable=gt, panel=panel,
                               user_timetables=current_user.timetables, selected_timetable_key=ut.id_)

    else:  # je neprihlaseny
        """
        ak je neprihlaseny:
            (pracuje sa s anonym. navstevnikom)
            vytvori prazdny rozvrh ( vratane panelu so vsetkym) a zobrazi ho
            dany rozvrh si zapamata do session"""  # TODO
        gt = Timetable([])
        panel = Panel()
        if request.method == 'POST':
            panel.check_forms()
        return render_template('timetable/timetable.html',
                               title='Rozvrh', web_header='Rozvrh',
                               timetable=gt, panel=panel)