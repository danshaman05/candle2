from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

from candle_backend import SERVER_PATH
from editable_timetable_manager.EditableTimetableManager import EditableTimetableManager
from timetable.Panel import Panel
from timetable.Timetable import Timetable

timetable = Blueprint('timetable', __name__)  # Blueprint instancia

@login_required
@timetable.route('/moj/rozvrh/<key>', methods=['GET'])
def user_timetable(key):
    key = int(key)

    ### EXPERIMENT
    etm = EditableTimetableManager.get_instance() # TODO nemusi byt Singleton
    etm.set_timetables(current_user)
    # etm = EditableTimetableManager(current_user)
    ### EXPERIMENT

    user_timetables = etm.get_timetables()

    # dany rozvrh ziskame z managera podla id:
    gt = etm.get_timetable(key)
    if gt is None:
        raise Exception("timetable cannot be None")

    # zobrazi rozvrh:
    panel = Panel()
    if request.method == 'POST':
        panel.check_forms()
    return render_template('timetable/timetable.html',
                           title=gt.name, web_header=gt.name,
                           timetable=gt, panel=panel,
                           user_timetables=user_timetables, selected_timetable_key=key)


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

        # EXPERIM
        etm = EditableTimetableManager.get_instance()   # TODO nemusi byt Singleton
        etm.set_timetables(current_user)
        # etm = EditableTimetableManager(current_user)
        ### EXPERIMENT


        # print(len(current_user.timetables))
        #ziskame prvy rozvrh
        gt, key = etm.get_first_timetable()
        if gt is None:
            raise Exception("timetable cannot be None")

        user_timetables = etm.get_timetables()

        # zobrazi rozvrh:
        panel = Panel()
        if request.method == 'POST':
            panel.check_forms()
        return render_template('timetable/timetable.html',
                               title=gt.name, web_header=gt.name,
                               timetable=gt, panel=panel, first_timetable_id=id,
                               user_timetables=user_timetables, selected_timetable_key=key)

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