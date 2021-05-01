from typing import List, Dict, Optional
from _collections import OrderedDict


from .PlacedLesson import PlacedLesson


class Timetable:
    """Class represents a timetable."""

    __lessons: List = None
    """list contains objects of model Lesson"""

    __layout: List = None
    """Layout is a three-dimensional list that represents a timetable layout. 
     It is a list of 5 lists - one for every day of the week. Every "day" is a list of "columns". Each column is a list of PlacedLessons.
    (days: List -> columns: List[PlacedLesson])"""

    __lessons_in_progress: List[List[Optional[str]]] = None

    # teaching times:
    __TIME_MIN = 490    # teaching starts at 8:10 (490 in minutes)
    __TIME_MAX = 1190
    __SHORTEST_LESSON = 45
    __SHORTEST_BREAKTIME = 5

    __starting_times: Dict[int, str] = {}   # TODO move to new data/CSV-file?
    """ List of starting times - times in which lessons usually starts at FMPH (from 8:10 to 19:00)
        Data format:
            key: time in minutes
            value: time in format H:MM
    """
    # List of starting times (from 8:10 to 19:00)
    __starting_times: List[str] = []

    __DAYS = "Pondelok, Utorok, Streda, Štvrtok, Piatok".split(',')     # TODO move to new folder data/CSV-file?
    """list of days of the week"""


    # Infolist URL:
    __INFOLIST_URL = 'https://sluzby.fmph.uniba.sk/infolist/SK/'  # TODO move to new data/CSV-file?

    def __init__(self, lessons=None):
        if lessons is None:
            raise Exception("Cannot create timetable without lessons!")
        self.__init_times()
        self.__lessons = lessons
        self.__init_layout()
        self.__set_layout()

    def __init_times(self):
        """
        Initialize __starting_times list ( starting_times are times when usualy starts lessons at FMFI / FMPH )
        """
        self.__starting_times = []
        for minutes in range(self.__TIME_MIN, self.__TIME_MAX, 50):
            self.__starting_times.append(self.minutes_2_time(minutes))

    def __init_layout(self):
        """ Initializes layout as a 2d list (day: List -> column: List )."""
        self.__layout = []
        for i in range(5):
            first_column = []
            self.__layout.append([first_column])

    def __init_last_started_lessons_list(self):
        """Initializes attribute __last_started_lessons"""
        self.__lessons_in_progress = []
        for di in range(len(self.__layout)):
            self.__lessons_in_progress.append([])
            for ci in range(len(self.__layout[di])):
                self.__lessons_in_progress[di].append(None)

    def __get_lessons_sorted_by_days(self):
        """Sorts all lessons by the days in the week. Each day is a list of lessons."""
        if self.__lessons is None:
            raise Exception("Attribute __lessons cannot be None")
        days: List[List] = []
        for i in range(5):  # 5 dni v tyzdni
            days.append([])
        for lesson in self.__lessons:
            days[lesson.day].append(lesson)
        return days

    def __set_layout(self):
        # TODO docstring
        """ Nastavi atribut self.__layout. Vlozi lessons do , tak, ze pre kazdy den vytvori
         pozadovany pocet stlpcov. Kazdy stlpec je OrderedDict. Algoritmus sa vzdy snazi pridavat hodiny
         do co "najviac laveho" stlpca. """
        lessons_sorted_by_days = self.__get_lessons_sorted_by_days()  # usporiadame si hodiny podla dni v tyzdni

        # Rozdelime hodiny do stlpcov:
        # pre kazdy den v tyzdni
        for day_index, lessons in enumerate(lessons_sorted_by_days):
            # pre kazdu hodinu v danom dni:
            for lesson in lessons:
                added = False
                column_index = 0
                while added == False:
                    if column_index == 6:
                        raise Exception("Cannot add more than 6 neighbour lessons in one day!")     # TODO catch exception & test this code!
                    # if we don't have enough columns, create a new one and place here lesson:
                    if len(self.__layout[day_index]) - 1 <  column_index:
                        new_column = [PlacedLesson(lesson, column_index)]
                        self.__layout[day_index].append(new_column)
                        break
                    # try to add the lesson:
                    if self.__can_add_lesson(lesson, self.__layout[day_index][column_index]):
                        self.__layout[day_index][column_index].append(PlacedLesson(lesson, column_index))
                        break
                    column_index += 1

    def __can_add_lesson(self, lesson, column: List):
        """Vrati True, ak sa hodina da vlozit do stlpca (neprebieha momentalne ina hodina v danom stlpci).
        Pre spravnu funkcnost musi byt column zoradeny podla casu."""

        if len(column) == 0:
            return True
        if self.__get_last_added_lesson(column).get_end() < int(lesson.start):
            return True
        return False

    def __get_last_added_lesson(self, column):
        """Vrati lesson, ktora bola naposledy pridana do daneho column."""
        return column[-1]


    def get_lessons(self):
        return self.__lessons

    def get_layout(self):
        return self.__layout

    def get_starting_times(self) -> List[str]:
        return self.__starting_times

    def get_days(self):
        """Returns list of days in the week."""
        return self.__DAYS


    @classmethod
    def get_infolist_url(cls, endpoint):
        return cls.__INFOLIST_URL + endpoint

    @classmethod
    def get_shortest_breaktime(cls):
        return cls.__SHORTEST_BREAKTIME

    @classmethod
    def get_shortest_lesson(cls):
        return cls.__SHORTEST_LESSON

    @classmethod
    def minutes_2_time(cls, time_in_minutes: int) -> str:
        """Return time in 24-hour format."""
        hours = time_in_minutes // 60
        minutes = time_in_minutes % 60
        return "%d:%02d" % (hours, minutes)
