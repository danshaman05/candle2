from sqlalchemy import or_

from candle_backend.models import Room, Teacher, StudentGroup
from timetable.forms import ShowLessonsForm, ShowTeachersForm, ShowRoomsForm, ShowStudentGroupsForm


class Panel:

    def __init__(self):
        self.__lessons_form = ShowLessonsForm()
        self.__teachers_form = ShowTeachersForm()
        self.__rooms_form = ShowRoomsForm()
        self.__student_groups_form = ShowStudentGroupsForm()

        self.__results = dict()  # vysledky hladania

    # FORMS:
    @property
    def lessons_form(self):
        return self.__lessons_form

    @property
    def teachers_form(self):
        return self.__teachers_form

    @property
    def rooms_form(self):
        return self.__rooms_form

    @property
    def student_groups_form(self):
        return self.__student_groups_form

    def set_results(self, list_of_objects, category):
        self.__results[category] = list_of_objects

    def get_results(self, category):
        """Vrati zoznam izieb. Ak sa kluc rooms nenachadza v self.__results, vrati None."""
        return self.__results.get(category)


    def __button_clicked(self, category) -> bool:
        # ak bol stlaceny button "Hladaj" pri rooms:
        if category == 'rooms':
            if self.__rooms_form.submit_rooms.data:
                return True
        elif category == 'teachers':
            if self.__teachers_form.submit_teachers.data:
                return True
        elif category == 'student_groups':
            if self.__student_groups_form.submit_groups.data:
                return True
        else:
            raise Exception('Wrong category parameter.')


    def check_forms(self):
        """skontroluje, ci bolo stlacene nejake tlacidlo z panela.
        Ak ano, tak spracuje danu poziadavku a nastavi vysledok v paneli. """

        if self.__button_clicked('rooms'):
            search = self.__rooms_form.show_rooms.data
            if search != '':  # TODO treba validovat string?
                search = search.replace(" ", "%")
                search = "%{}%".format(search)
                rooms_list = Room.query.filter(Room.name.like(search)).all()    # TODO pouzit ilike?
                self.set_results(rooms_list, 'rooms')

        elif self.__button_clicked('teachers'):
            search = self.__teachers_form.show_teachers.data
            if search != '':
                print("SEARCH: ", search)

                search = search.replace(" ", "%")
                search = search.replace(".", "%")
                search = "%{}%".format(search)

                teachers = Teacher.query.filter(
                    or_( Teacher.fullname.like(search),
                         Teacher.fullname_reversed.like(search)) )\
                    .order_by(Teacher.family_name)\
                    .limit(50).all()

                self.set_results(list(teachers), 'teachers')

        elif self.__button_clicked('student_groups'):
            search = self.__student_groups_form.show_student_groups.data
            if search != '':
                search = search.replace(" ", "%")
                search = "%{}%".format(search)
                groups_list = StudentGroup.query.filter(StudentGroup.name.ilike(search)).all()
                print(len(groups_list))
                self.set_results(groups_list, 'student_groups')
