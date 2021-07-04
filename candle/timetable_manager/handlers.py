from flask import Blueprint, request, url_for, jsonify, render_template
from flask_login import current_user, login_required
from candle import db
from candle.models import UserTimetable, Teacher, Room, StudentGroup, Lesson, Subject
import re
from candle.timetable.timetable import Timetable, TooManyColumnsError

timetable_manager = Blueprint('timetable_manager',
                              __name__,
                              static_folder='static',
                              static_url_path='/timetable_manager/static')


@login_required
@timetable_manager.route('/add_or_remove_lesson', methods=['POST'])
def add_or_remove_lesson():
    """Add/Remove lesson to/from user's timetable. Return timetable templates (layout & list)."""
    lesson_id = request.form.get('lesson_id')
    action = request.form.get('action')
    window_pathname = request.form.get('window_pathname')
    timetable_id = window_pathname.split('/')[-1]
    ut = UserTimetable.query.get(timetable_id)
    lesson = Lesson.query.get(lesson_id)

    if action == 'add':
        ut.lessons.append(lesson)
    elif action == 'remove':
        ut.lessons.remove(lesson)
    else:
        raise Exception("Bad JSON data format! Value for 'action' should be 'add' or 'remove'.")
    db.session.commit()

    try:
        t = Timetable(lessons=ut.lessons.order_by(Lesson.day, Lesson.start).all())
    except TooManyColumnsError:
        return jsonify({'success': 0})

    timetable_layout = render_template('timetable/timetable_content.html', timetable=t)
    timetable_list = render_template('timetable/list.html', timetable=t)

    return jsonify({'success':1, 'layout_html': timetable_layout,
                    'list_html': timetable_list})



@login_required
@timetable_manager.route('/add_or_remove_subject', methods=['POST'])
def add_or_remove_subject():
    """Add/Remove subject (with all lessons) to/from user's timetable. Return timetable templates (layout & list)."""
    subject_id = request.form.get('subject_id')
    action = request.form.get('action')
    window_pathname = request.form.get('window_pathname')
    timetable_id = window_pathname.split('/')[-1]  # TODO it's not the best idea to rely just on the URL path... maybe we need state-management
    ut = UserTimetable.query.get(timetable_id)
    subject = Subject.query.get(subject_id)

    if action == 'add':
        for l in subject.lessons:
            if l not in ut.lessons:
                ut.lessons.append(l)
    elif action == 'remove':
        for l in subject.lessons:
            ut.lessons.remove(l)
    else:
        raise Exception("Bad JSON data format! Value for 'action' should be 'add' or 'remove'.")
    db.session.commit()
    t = Timetable(lessons=ut.lessons.order_by(Lesson.day, Lesson.start).all())

    timetable_layout = render_template('timetable/timetable_content.html', timetable=t)
    timetable_list = render_template('timetable/list.html', timetable=t)

    return jsonify({'layout_html': timetable_layout,
                    'list_html': timetable_list})
