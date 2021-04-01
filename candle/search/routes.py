# This blueprint contains AJAX routes that corresponds to the search panels

from flask import Blueprint, request, jsonify
from sqlalchemy import or_

from ..models import Teacher

search = Blueprint('search', __name__)



@search.route('/get_teachers_list', methods=['GET'])
def get_teachers_list():
    query_string = request.args['term']         # TODO: request could be JSON

    query_string = query_string.replace(" ", "%")
    query_string = query_string.replace(".", "%")
    query_string = "%{}%".format(query_string)

    teachers = Teacher.query.filter(
        or_(Teacher.fullname.like(query_string),
            Teacher.fullname_reversed.like(query_string))) \
        .order_by(Teacher.family_name) \
        .limit(50).all()

    array = []
    for t in teachers:
        array.append({'id':t.slug, 'value':t.fullname})     # do not change key names (jquery-ui autocomplete widget will not work)

    return jsonify(array)  # we are sending teacher slug and fullname


@search.route('/get_rooms_list', methods=['GET'])
def get_rooms_list():
    # TODO
    pass
