# This blueprint contains AJAX routes that corresponds to the search inputs

from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from candle.models import Teacher, Room, StudentGroup

search = Blueprint('search', __name__)


@search.route('/get_data/teachers', methods=['GET'])
def get_teachers_json():
    """Find all teachers by query string typed in the search bar and send them back in a JSON.

    Function will get data from the URL parameter sended from the JQueryUI Autocomplete search bar and will respond
    with the JSON that will contain a list of teachers.

    Request URL format: /get_data/teachers?term=query, where query is a string typed in the search bar.
    Respond JSON format: list, where every element is a dictionary {'id':teacher.slug, 'value':teacher.fullname}.
    """
    query_string = request.args.get('term')
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
        array.append({'id': t.slug, 'value': t.fullname})     # do not change key names ('id' and 'value')! (the jquery-ui autocomplete widget will not work)
    return jsonify(array)

@search.route('/get_data/rooms', methods=['GET'])
def get_rooms_json():
    """Find all rooms by query string typed in the search bar and send them back in a JSON.

    Function will get data from the URL parameter sended from the JQueryUI Autocomplete search bar and will respond
    with the JSON that will contain a list of rooms.

    Request URL format: /get_data/rooms?term=query, where query is a string typed in the search bar.
    Respond JSON format: list, where every element is a dictionary {'id':room.name, 'value':room.name}.
    """
    query_string = request.args.get('term')
    query_string = query_string.replace(" ", "%")
    query_string = "%{}%".format(query_string)
    rooms = Room.query.filter(Room.name.like(query_string)).limit(50).all()

    array = []
    for r in rooms:
        array.append({'id': r.name, 'value': r.name})
    return jsonify(array)

@search.route('/get_data/groups', methods=['GET'])
def get_groups_json():
    """Find all student groups by query string typed in the search bar and send them back in a JSON.

    Function will get data from the URL parameter sended from the JQueryUI Autocomplete search bar and will respond
    with the JSON that will contain a list of student groups.

    Request URL format: /get_data/groups?term=query, where query is a string typed in the search bar.
    Respond JSON format: list, where every element is a dictionary {'id':group.name, 'value':group.name}.
    """
    query_string = request.args.get('term')
    query_string = query_string.replace(" ", "%")
    query_string = "%{}%".format(query_string)
    groups = StudentGroup.query.filter(StudentGroup.name.like(query_string)).limit(50).all()

    array = []
    for g in groups:
        array.append({'id': g.name, 'value': g.name})
    return jsonify(array)


