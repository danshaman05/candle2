from typing import Union

from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

from candle import db, login_manager
from candle.timetable.layout import Layout

class Entity(db.Model):
    """Abstract class for Room, Student-Group and Teacher."""
    __abstract__ = True

    @property
    def url_id(self) -> Union[str, int]:
        if '.' in self.name or '_' in self.name:     # TODO add more problematic characters if necessary
            return self.id_
        return self.name


class Room(Entity):
    id_ = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(30), nullable=False)
    room_type_id = db.Column(db.Integer, db.ForeignKey('room_type.id'), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    lessons = db.relationship('Lesson', backref='room',
                              lazy='dynamic')  # 'lazy dynamic' allows us to work with lessons attribute like with query ( we can run order_by, etc)

    @property
    def prefix(self):
        # xMieRez is a special case:
        if 'xMieRez' in self.name:
            return "Ostatné"

        first_dash_position = self.name.find('-')
        if first_dash_position == -1:  # name doesn't contain '-'
            return self.name
        return self.name[0 : first_dash_position]

    def __repr__(self):
        return "<Room %r>" % self.name


teacher_lessons = db.Table('teacher_lessons',
                           db.Column('id', db.Integer, primary_key=True),
                           db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id')),
                           db.Column('lesson_id', db.Integer, db.ForeignKey('lesson.id')))

class Teacher(Entity):
    id_ = db.Column('id', db.Integer, primary_key=True)
    given_name = db.Column(db.String(50), nullable=True)
    family_name = db.Column(db.String(50), nullable=False)
    iniciala = db.Column(db.String(50), nullable=True)
    oddelenie = db.Column(db.String(), nullable=True)
    katedra = db.Column(db.String(), nullable=True)
    external_id = db.Column(db.String(), nullable=True)
    login = db.Column(db.String(), nullable=True)
    slug = db.Column(db.String(), nullable=True)
    lessons = db.relationship('Lesson', secondary=teacher_lessons, lazy='dynamic',
                              backref=db.backref('teachers', lazy='joined', order_by="asc(Teacher.family_name)"))
    def __repr__(self):
        return f"Teacher(id:'{self.id_}', :'{self.given_name} {self.family_name}' )"

    @property
    def short_name(self):
        """E.g. for 'Andrej Blaho' return 'A. Blaho'"""
        if self.given_name is None or self.given_name.strip() == '':
            return self.family_name
        return self.given_name[0] + ". " + self.family_name

    @hybrid_property
    def fullname(self):
        return self.given_name + " " + self.family_name

    @hybrid_property    # we need it in SQL queries
    def fullname_reversed(self):
        return self.family_name + " " + self.given_name


student_group_lessons = db.Table('student_group_lessons',
                                 db.Column('student_group_id', db.Integer, db.ForeignKey('student_group.id')),
                                 db.Column('lesson_id', db.Integer, db.ForeignKey('lesson.id')))


class StudentGroup(Entity):
    id_ = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    lessons = db.relationship('Lesson', secondary=student_group_lessons, lazy='dynamic')



class Lesson(db.Model):
    id_ = db.Column('id', db.Integer, primary_key=True)
    day = db.Column(db.Integer, nullable=False)
    start = db.Column(db.Integer, nullable=False)
    end = db.Column(db.Integer, nullable=False)
    lesson_type_id = db.Column(db.Integer, db.ForeignKey('lesson_type.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    external_id = db.Column(db.Integer, nullable=True)
    note = db.Column(db.VARCHAR, nullable=True)

    def __repr__(self):
        return f"Lesson(id:'{self.id_}', room_id:'{self.room_id}' )"

    @property
    def day_abbreviated(self) -> str:
        """Returns abbreviation of the day of the week."""
        days = ['Po', 'Ut', 'St', 'Št', 'Pi']
        return days[self.day]

    @property
    def start_formatted(self):
        return Layout.minutes_2_time(self.start)

    @property
    def end_formatted(self):
        return Layout.minutes_2_time(self.end)

    @property
    def breaktime(self) -> int:
        hours_count = self.rowspan
        return int(Layout.get_shortest_breaktime() * hours_count)

    @property
    def rowspan(self) -> int:
        """Return how many rows takes lesson in the timetable."""
        return (self.end - self.start) // Layout.get_shortest_lesson()

    def get_teachers_formatted(self):
        """ Return teachers separated by commas.
        E.g.: "A. Blaho, D. Bezáková, A. Hrušecká"
        """
        return ', '.join([t.short_name for t in self.teachers])


class LessonType(db.Model):
    id_ = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    code = db.Column(db.String(1), nullable=False)
    lessons = db.relationship('Lesson', backref='type', lazy=True)

    def __repr__(self):
        return f"{self.name}"


class Subject(db.Model):
    id_ = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), nullable=False)
    short_code = db.Column(db.String(20), nullable=False)
    credit_value = db.Column(db.Integer, nullable=False)
    rozsah = db.Column(db.String(30), nullable=True)
    external_id = db.Column(db.String(30), nullable=True)
    lessons = db.relationship('Lesson', backref='subject', lazy=True)

    def __repr__(self):
        return f"Subject(id:'{self.id_}', name:'{self.name}' )"


class RoomType(db.Model):
    id_ = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    code = db.Column(db.String(1), nullable=False)


user_timetable_lessons = db.Table('user_timetable_lessons',
                                  db.Column('id', db.Integer(), primary_key=True),
                                  db.Column('user_timetable_id', db.Integer, db.ForeignKey('user_timetable.id')),
                                  db.Column('lesson_id', db.Integer, db.ForeignKey('lesson.id')),
                                  db.Column('highlighted', db.Boolean, default=False))


class UserTimetable(db.Model):
    id_ = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    published = db.Column(db.Integer, default=0)
    slug = db.Column(db.String(30))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    lessons = db.relationship('Lesson',
                              secondary=user_timetable_lessons,
                              backref=db.backref('user_timetable', lazy='joined'),
                              lazy='dynamic')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True)
    timetables = db.relationship('UserTimetable', backref='owner', lazy='dynamic')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


######################################################
# TODO:
@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'
