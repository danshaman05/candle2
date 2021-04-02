# This blueprint contains AJAX routes that corresponds to the search panels

from flask import Blueprint, request, jsonify
from sqlalchemy import or_

from candle.models import Teacher, Room, StudentGroup

search = Blueprint('search', __name__)



@search.route('/get_data/teachers', methods=['GET'])
def get_teachers_json():
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
    # send the teacher's slug and fullname via JSON:
    for t in teachers:
        array.append({'id': t.slug, 'value': t.fullname})     # do not change key names ('id' and 'value')! (the jquery-ui autocomplete widget will not work)
    return jsonify(array)


@search.route('/get_data/rooms', methods=['GET'])
def get_rooms_json():
    query_string = request.args['term']
    query_string = query_string.replace(" ", "%")
    query_string = "%{}%".format(query_string)
    rooms = Room.query.filter(Room.name.like(query_string)).limit(50).all()
    array = []
    for r in rooms:
        array.append({'id': r.name, 'value': r.name})
    return jsonify(array)



@search.route('/get_data/groups', methods=['GET'])
def get_groups_json():
    query_string = request.args['term']
    query_string = query_string.replace(" ", "%")
    query_string = "%{}%".format(query_string)
    groups = StudentGroup.query.filter(StudentGroup.name.like(query_string)).limit(50).all()
    array = []
    for g in groups:
        array.append({'id': g.name, 'value': g.name})
    return jsonify(array)


