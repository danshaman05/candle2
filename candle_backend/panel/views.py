from flask import Blueprint, request

panel = Blueprint('panel', __name__)  # Blueprint instancia


@panel.route('/search_teacher', methods=['POST'])
def search_teacher():
    query = request.form['data']
