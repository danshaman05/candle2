from flask import Blueprint

from candle_backend import temporary_path

timetable = Blueprint('timetable', __name__)    # Blueprint instancia


@timetable.route(temporary_path + '/', methods=['GET', 'POST'])
def home():
    """
    ak je prihlaseny:

    ak je neprihlaseny:
        vytvori anonymneho navstevnika (neuklada sa do DB, je iba v session)
        vytvori mu prazdny rozvrh a zobrazi ho
        zobrazuje aj panel so vsetkym

    """
    pass


    # return f'<a href="{temporary_path}/miestnosti">Rozvrhy všetkých miestností</a>' \
    #        f'<br><a href="{temporary_path}/ucitelia">Rozvrhy všetkých učiteľov</a>' \
    #        f'<br><a href="{temporary_path}/kruzky">Rozvrhy všetkých krúžkov</a>'