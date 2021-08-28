'''
Project: Candle (New Generation): Candle rewrite from PHP to Python.
Author: Daniel Grohol, FMFI UK
'''


from flask import Blueprint, request, jsonify
from candle.models import Teacher, Room, StudentGroup, Subject, Lesson, teacher_lessons

api = Blueprint('api', __name__)


@api.route('/api/teachers')
def get_teachers():
    """Find all teachers by query string and send them back in a JSON.

    Function will get data from the URL parameter and will respond
    with the JSON that will contain a list of teachers.

    Request URL format: /get_data/teachers?term=query, where query is a substring from teacher's name.
    Respond JSON format: list, where every element is a dictionary {'id':teacher.slug, 'value':teacher.fullname}.
    """
    query_string = request.args.get('term')
    query_string = query_string.replace(" ", "%")
    query_string = query_string.replace(".", "%")
    query_string = "%{}%".format(query_string)

    teachers = Teacher.query.filter(
        Teacher.fullname.ilike(query_string) | Teacher.fullname_reversed.ilike(query_string))\
        .order_by(Teacher.family_name) \
        .limit(50).all()

    array = []
    for t in teachers:
        array.append({'id': t.slug, 'value': t.fullname})     # do not change key names ('id' and 'value')! (the jquery-ui autocomplete widget will not work)
    return jsonify(array)


@api.route('/api/rooms')
def get_rooms():
    """Find all rooms by query string and send them back in a JSON.

    Function will get data from the URL parameter and will respond
    with the JSON that will contain a list of rooms.

    Request URL format: /get_data/rooms?term=query, where query is a substring from room's name.
    Respond JSON format: list, where every element is a dictionary {'id':room.name, 'value':room.name}.
    """
    query_string = request.args.get('term')
    query_string = query_string.replace(" ", "%")
    query_string = "%{}%".format(query_string)
    rooms = Room.query.filter(Room.name.ilike(query_string)).limit(50).all()

    array = []
    for r in rooms:
        array.append({'id': r.name, 'value': r.name})
    return jsonify(array)


@api.route('/api/groups')
def get_groups():
    """Find all student groups by query string and send them back in a JSON.

    Function will get data from the URL parameter and will respond
    with the JSON that will contain a list of student groups.

    Request URL format: /get_data/groups?term=query, where query is a substring from group's name.
    Respond JSON format: list, where every element is a dictionary {'id':group.name, 'value':group.name}.
    """
    query_string = request.args.get('term')
    query_string = query_string.replace(" ", "%")
    query_string = "%{}%".format(query_string)
    groups = StudentGroup.query.filter(StudentGroup.name.ilike(query_string)).limit(50).all()

    array = []
    for g in groups:
        array.append({'id': g.name, 'value': g.name})
    return jsonify(array)
