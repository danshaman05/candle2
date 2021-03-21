from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

from . import db, login_manager
from .timetable.Timetable import Timetable


class Room(db.Model):
    id_ = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    room_type_id = db.Column(db.Integer, db.ForeignKey('room_type.id'), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    lessons = db.relationship('Lesson', backref='room',
                              lazy='dynamic')  # vdaka dynamic mozme s lessons pracovat ako s query (mozme spustit order_by,...)

    def __repr__(self):
        return "<Room %r>" % self.name


teacher_lessons = db.Table('teacher_lessons',
                           db.Column('id', db.Integer, primary_key=True),
                           db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id')),
                           db.Column('lesson_id', db.Integer, db.ForeignKey('lesson.id'))
                           )


class Teacher(db.Model):
    id_ = db.Column('id', db.Integer, primary_key=True)
    given_name = db.Column(db.String(50), nullable=True)
    family_name = db.Column(db.String(50), nullable=False)
    iniciala = db.Column(db.String(50), nullable=True)
    oddelenie = db.Column(db.String(), nullable=True)
    katedra = db.Column(db.String(), nullable=True)
    external_id = db.Column(db.String(), nullable=True)
    login = db.Column(db.String(), nullable=True)
    slug = db.Column(db.String(), nullable=True)
    lessons = db.relationship('Lesson', secondary=teacher_lessons, backref=db.backref('teachers', lazy='joined'),
                              lazy='dynamic')

    # fullname = column_property(given_name + " " + family_name)

    def __repr__(self):
        return f"Teacher(id:'{self.id}', :'{self.given_name} {self.family_name}' )"

    @property
    def short_name(self):
        """Vrati skratene meno, napr. pre "Andrej Blaho" vrati "A. Blaho" """
        if self.given_name == '':  # Napr. teacher id 1259
            return ''
        return self.given_name[0] + ". " + self.family_name

    @hybrid_property
    def fullname(self):
        return self.given_name + " " + self.family_name

    @hybrid_property    # pouzivame ich v SQL queries, preto su hybrid
    def fullname_reversed(self):
        return self.family_name + " " + self.given_name


student_group_lessons = db.Table('student_group_lessons',
                                 db.Column('student_group_id', db.Integer, db.ForeignKey('student_group.id')),
                                 db.Column('lesson_id', db.Integer, db.ForeignKey('lesson.id')))



class StudentGroup(db.Model):
    id_ = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    lessons = db.relationship('Lesson', secondary=student_group_lessons, lazy='dynamic')    # LAZY OVERENE


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

    def get_day_abbr(self) -> str:
        """Vrati skratku dna v tyzdni (abbreviation)."""
        days = ['Po', 'Ut', 'St', 'Št', 'Pi']
        return days[self.day]

    def get_start(self):
        return Timetable.minutes_2_time(self.start)

    def get_end(self):
        return Timetable.minutes_2_time(self.end)

    def get_breaktime(self) -> int:
        hours_count = self.get_rowspan()
        return int(Timetable.get_shortest_breaktime() * hours_count)

    def get_rowspan(self) -> int:
        return (self.end - self.start) // Timetable.get_shortest_lesson()


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
    lessons = db.relationship('Lesson', backref='subject',
                              lazy='joined')  # lazy=True znamena, ze sa lessons nacitaju iba pri volani

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


# TODO:
@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'
