from timetable.Timetable import Timetable


class EditableTimetable(Timetable):

    def __init__(self, user_timetable):
        super().__init__(user_timetable.lessons)
        self.timetable = user_timetable
        self.name = user_timetable.name

    def set_key(self, key):
        self.key = key