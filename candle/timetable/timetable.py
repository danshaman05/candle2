from flask import Blueprint

timetable = Blueprint('timetable',
                      __name__,
                      template_folder='templates')