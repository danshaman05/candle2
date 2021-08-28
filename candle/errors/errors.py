'''
Project: Candle (New Generation): Candle rewrite from PHP to Python.
Author: Daniel Grohol
'''

from flask import Blueprint, render_template
from flask_wtf.csrf import CSRFError

errors = Blueprint('errors',
                   __name__,
                   template_folder='templates')

@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404

@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403

@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500

@errors.app_errorhandler(CSRFError)
def csrf_error(reason):
    return render_template('errors/csrf_error.html', reason=reason.description), 400
