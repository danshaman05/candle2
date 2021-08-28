'''
Project: Candle (New Generation): Candle rewrite from PHP to Python.
Author: Daniel Grohol, FMFI UK
'''

from flask import Blueprint

panel = Blueprint('panel',
                  __name__,
                  static_folder='static',
                  template_folder='templates',
                  static_url_path='/panel/static')
