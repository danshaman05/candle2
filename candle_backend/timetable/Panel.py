from timetable.forms import ShowLessonsForm, ShowTeachersForm, ShowRoomsForm, ShowStudentGroupsForm


class Panel:

    def __init__(self):
        self.__lessons_form = ShowLessonsForm()
        self.__teachers_form = ShowTeachersForm()
        self.__rooms_form = ShowRoomsForm()
        self.__student_groups_form = ShowStudentGroupsForm()

    @property
    def lessons_form(self):
        return self.__lessons_form

    @property
    def teachers_form(self):
        return self.__lessons_form

    @property
    def rooms_form(self):
        return self.__lessons_form

    @property
    def student_groups_form(self):
        return self.__lessons_form
