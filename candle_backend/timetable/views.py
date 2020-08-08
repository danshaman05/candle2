from flask import Blueprint, render_template, request
from flask_login import current_user

from candle_backend import temporary_path
from timetable.Panel import Panel
from timetable.Timetable import Timetable

timetable = Blueprint('timetable', __name__)  # Blueprint instancia


@timetable.route(temporary_path + '/', methods=['GET', 'POST'])
def home():
    """
    ak je prihlaseny:
        ak ma nejake rozvrhy:
            zobrazi rozvrh daneho usera - vyberie nahodne   #TODO dorobit prepinanie rozvrhov
        inak:
            vytvori prazdny rozvrh a priradi ho uzivatelovi


    ak je neprihlaseny:
        (pracuje sa s anonym. navstevnikom)
        vytvori prazdny rozvrh ( vratane panelu so vsetkym) a zobrazi ho
        dany rozvrh si zapamata do session
    """
    # ak je prihlaseny:
    if current_user.is_authenticated:
        # ak ma nejake rozvrhy:
        timetables = current_user.timetables
        if timetables:
            # ziska nejaky jeho rozvrh:
            ut = timetables[0]
            # vytvori graficky rozvrh:
            gt = Timetable(ut.lessons)

            # zobrazi rozvrh:
            panel = Panel()
            if request.method == 'POST':
                panel.check_forms()
            return render_template('timetable/timetable.html',
                                   title=ut.name, web_header=ut.name,
                                   timetable=gt, panel=panel)
        else:
            pass  # TODO vytvorit mu rozvrh a priradit mu ho



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