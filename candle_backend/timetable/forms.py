from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length


class ShowLessonsForm(FlaskForm):
    show_lessons = StringField('showLessons')  # Length(max=30, message="Zadajte názov predmetu"))
    submit = SubmitField('Hľadaj')


class ShowTeachersForm(FlaskForm):
    show_teachers = StringField('showTeachers')  # Length(max=30, message="Zadajte názov predmetu"))
    submit = SubmitField('Hľadaj')


class ShowRoomsForm(FlaskForm):
    show_rooms = StringField('showRooms') #, Length(min=1, max=30, message="Zadajte názov predmetu"))
    submit = SubmitField('Hľadaj')


class ShowStudentGroupsForm(FlaskForm):
    show_student_groups = StringField('showStudentGroups')  # Length(max=30, message="Zadajte názov predmetu"))
    submit = SubmitField('Hľadaj')