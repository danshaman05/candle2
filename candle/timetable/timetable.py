'''
Project: Candle (New Generation): Candle rewrite from PHP to Python.
Author: Daniel Grohol, FMFI UK
'''

from flask import Blueprint, make_response

timetable = Blueprint('timetable',
                      __name__,
                      template_folder='templates',
                      static_folder='static',
                      static_url_path='/timetable/static')

def get_lessons_as_csv_response(layout, filename):
    """Return response as CSV file where data corresponds with a timetable's list of lessons."""
    # headers:
    csv = [';'.join(layout.get_list_headers())]
    # data from list of lessons:
    for lesson in layout.get_lessons():
        row = []
        row.append(str(lesson.day_abbreviated))
        row.append(str(lesson.start_formatted))
        row.append(str(lesson.end_formatted))
        row.append(str(lesson.room.name))
        row.append(str(lesson.type))
        row.append(str(lesson.subject.short_code))
        row.append(str(lesson.subject.name))
        row.append(str(lesson.get_teachers_formatted()))
        row.append(str(lesson.get_note()))
        row_formatted = ';'.join(row)
        csv.append(row_formatted)

    csv = '\n'.join(csv)

    response = make_response(csv)
    cd = f'attachment; filename={filename}.csv'
    response.headers['Content-Disposition'] = cd
    response.mimetype='text/csv'
    return response