from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class ShowLessonsForm(FlaskForm):
    show_lessons = StringField('showLessons')  # Length(max=30, message="Zadajte názov predmetu"))  # TODO nastavit length?
    submit_lessons = SubmitField('Hľadaj')


class ShowTeachersForm(FlaskForm):
    show_teachers = StringField('showTeachers')  # Length(max=30, message="Zadajte názov predmetu"))
    submit_teachers = SubmitField('Hľadaj')


class ShowRoomsForm(FlaskForm):
    show_rooms = StringField('showRooms') #, Length(min=1, max=30, message="Zadajte názov predmetu"))
    submit_rooms = SubmitField('Hľadaj')


class ShowStudentGroupsForm(FlaskForm):
    show_student_groups = StringField('showStudentGroups')
    submit_groups = SubmitField('Hľadaj')