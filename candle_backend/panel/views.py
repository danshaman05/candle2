from flask import Blueprint, request

panel = Blueprint('panel', __name__)  # Blueprint instancia


@panel.route('/search_teacher', methods=['POST'])
def search_teacher():
    query = request.form['data']


# @panel.route('/search_room', methods=['POST'])
# def search_room():
#     query = request.form['data']
#
#
# @panel.route('/search_group', methods=['POST'])
# def search_group():
#     query = request.form['data']