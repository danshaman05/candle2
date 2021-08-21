"""This blueprint contains AJAX routes that corresponds to the search function."""

from flask import Blueprint, request, jsonify, render_template
from flask_login import current_user

from candle.models import Teacher, Room, StudentGroup, Lesson, teacher_lessons, Subject, UserTimetable

search = Blueprint('search',
                   __name__,
                   template_folder='templates',
                   static_folder='static',
                   static_url_path='/search/static')


@search.route('/subject_search_handler')
def subject_search_handler():
    """Find and return all subjects by subject name or short-code, teachers by name (also reversed name) and rooms by room name.

    Request URL format: /subject_search_handler?term=query, where query is a substring from a one of above listed choices.
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


@search.route('/get_html/lessons_list', methods=['POST'])
def lessons_list():
    """
    Return HTML template with the list of subjects and lessons for the search function.
    """
    item_id = request.form.get('item-id')
    item_category = request.form.get('item-category')
    pathname = request.form.get('pathname')
    pathname_list = pathname.split('/')

    # Check, if we can show add/remove checkboxes:
    show_checkboxes, timetable_lessons = False, []     # init variables
    if "moj-rozvrh" in pathname_list and current_user.is_authenticated:   # if we are on the user's timetable route:
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


    return render_template('search/subject_search-results.html', subjects=subjects,
                           show_checkboxes=show_checkboxes, timetable_lessons=timetable_lessons)

