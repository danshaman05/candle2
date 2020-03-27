from flask import render_template
from candle_backend.models import Room
from candle_backend import app
from candle_backend.helpers import getRoomsSortedByDashes_dict


@app.route('/')
def list_all_rooms():
    rooms = Room.query.all()
    rooms_dict = getRoomsSortedByDashes_dict(rooms)  # ucebne su v jednom dictionary rozdelene podla prefixu

    return render_template('rooms.html', rooms_dict=rooms_dict)
