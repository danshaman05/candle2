"""This blueprint contains AJAX routes that corresponds to the search function."""

from flask import Blueprint, request, jsonify, render_template
from candle.models import Teacher, Room, StudentGroup, Lesson, teacher_lessons, Subject, UserTimetable

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
        Teacher.fullname.ilike(query_string) | Teacher.fullname_reversed.ilike(query_string))\
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
    rooms = Room.query.filter(Room.name.ilike(query_string)).limit(50).all()

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
    groups = StudentGroup.query.filter(StudentGroup.name.ilike(query_string)).limit(50).all()

    array = []
    for g in groups:
        array.append({'id': g.name, 'value': g.name})
    return jsonify(array)


@search.route('/get_data/lesson_search')
def lesson_search_handler():
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


@search.route('/get_html/lessons_list', methods=['POST'])
def lessons_list():
    """
    Return HTML template with the list of subjects and lessons for the panel search.
    """
    item_id = request.form.get('item-id')
    item_category = request.form.get('item-category')
    pathname = request.form.get('pathname')
    pathname_list = pathname.split('/')

    #Let's check, if we can show add/remove checkboxes:
    show_checkboxes, timetable_lessons = False, []     # init variables
    if "moj-rozvrh" in pathname_list:   # if we are on the user's timetable route:
        show_checkboxes = True
        # get lessons of the current user's timetable:
        current_timetable_id = pathname_list[-1]
        ut = UserTimetable.query.get(current_timetable_id)
        timetable_lessons = ut.lessons.all()

    subjects = []
    if item_category == 'Predmety':
        subjects = Subject.query.filter(Subject.name == item_id)\
            .order_by(Subject.name).all()

    elif item_category == 'Učitelia':
        subjects = Subject.query.join(Lesson).join(teacher_lessons).join(Teacher)\
            .filter(Teacher.slug == item_id).all()

    elif item_category == 'Miestnosti':
        subjects = Subject.query.join(Lesson).join(Room)\
            .filter(Room.name == item_id)\
            .order_by(Subject.name).all()

    elif item_category == 'Kódy predmetov':
        subjects = Subject.query.filter(Subject.short_code == item_id)\
            .order_by(Subject.short_code).all()


    return render_template('panel/lessons-search_results.html', subjects=subjects,
                           show_checkboxes=show_checkboxes, timetable_lessons=timetable_lessons)

