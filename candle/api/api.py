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




@api.route('/api/subjects')
def get_subjects():
    """Find all subjects by subject name, subject teacher name, subject room name or subject short-code.

    Request URL format: /api/subjects?term=query, where query is a substring from a one of above listed choices.
    Respond JSON format: list, where every element is a subject, subject's short-code, teacher's name or a room's name.
    """
    query_string = request.args.get('term')
    query_string = query_string.replace(" ", "%")
    query_string = "%{}%".format(query_string)

    # Select unique subject names (each subject must have at least one lesson, so we join with Lessons):
    subjects = Subject.query.join(Lesson).filter(Subject.name.ilike(query_string))\
        .with_entities(Subject.name).distinct()\
        .order_by(Subject.name)\
        .limit(20).all()

    # Search in subject short-codes:
    subjects_c = Subject.query.join(Lesson).filter(Subject.short_code.ilike(query_string))\
        .with_entities(Subject.short_code).distinct()\
        .order_by(Subject.short_code)\
        .limit(20).all()

    # Search in teachers who have at least one lesson (filter out those who don't have a given_name):
    teachers = Teacher.query.join(teacher_lessons).join(Lesson) \
        .filter(Teacher.given_name != '') \
        .filter(Teacher.fullname.ilike(query_string) | Teacher.fullname_reversed.ilike(query_string))\
        .order_by(Teacher.family_name) \
        .limit(20).all()

    # Search in rooms that have at least one lesson:
    rooms = Room.query.join(Lesson)\
        .with_entities(Room.name).distinct()\
        .filter(Room.name.ilike(query_string))\
        .order_by(Room.name)\
        .limit(20).all()

    array = []
    for s in subjects:
        array.append({'id': s.name, 'label': s.name, 'category': 'Predmety'})
    for s in subjects_c:
        array.append({'id': s.short_code, 'label': s.short_code, 'category': 'Kódy predmetov'})
    for t in teachers:
        array.append({'id': t.slug, 'label': t.fullname, 'category': 'Učitelia'})
    for r in rooms:
        array.append({'id': r.name, 'label': r.name, 'category': 'Miestnosti'})

    return jsonify(array)
