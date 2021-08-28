'''
Project: Candle (New Generation): Candle rewrite from PHP to Python.
Author: Daniel Grohol, FMFI UK
'''

from flask import Blueprint

timetable = Blueprint('timetable',
                      __name__,
                      template_folder='templates')
