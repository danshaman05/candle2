from flask import Blueprint
from flask_login import current_user

from candle_backend import temporary_path

timetable = Blueprint('timetable', __name__)    # Blueprint instancia


@timetable.route(temporary_path + '/', methods=['GET', 'POST'])
def home():
    """
    ak je prihlaseny:
        ak ma rozvrhy nejake:
            zobrazi rozvrh daneho usera - vyberie nahodne
        inak:
            vytvori prazdny rozvrh a priradi ho uzivatelovi


    ak je neprihlaseny:
        vytvori anonymneho navstevnika (neuklada sa do DB, je iba v session)
        vytvori mu prazdny rozvrh a zobrazi ho
        zobrazuje aj panel so vsetkym

    """
    # ak je prihlaseny:
    # if current_user.is_authenticated:
        # ak ma nejake rozvrhy:


    return 'NIC'