"""This blueprint contains AJAX routes that corresponds to the search function."""

from flask import Blueprint, request, jsonify, render_template
from flask_login import current_user

from candle.models import Teacher, Room, StudentGroup, Lesson, teacher_lessons, Subject, UserTimetable

search = Blueprint('search',
                   __name__,
                   template_folder='templates',
                   static_folder='static',
                   static_url_path='/search/static')


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


    return render_template('search/lessons-search_results.html', subjects=subjects,
                           show_checkboxes=show_checkboxes, timetable_lessons=timetable_lessons)

