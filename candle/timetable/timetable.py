from typing import List, Dict, Optional
from _collections import OrderedDict


class Timetable:
    """Class represents a timetable."""

    __lessons: List = None
    """list contains objects of model Lesson"""

    __layout: List = None
    """Layout is a two-dimensional list which represents a timetable layout. 
     It is a list of 5 lists - one for every day of the week. Every "day" is a list of "columns". Each column 
    is represented by one OrderedDict which maps starting times to the lesson objects. 
    (days: List -> columns: List[OrderedDict])
    Note, that we use OrderedDict instead of dict, because the order of the lessons added to it is important in our algorithm. """

    __lessons_in_progress: List[List[Optional[str]]] = None

    # teaching times:
    __TIME_MIN = 490    # teaching starts at 8:10 (=490 in minutes)
    __TIME_MAX = 1190
    __SHORTEST_LESSON = 45
    __SHORTEST_BREAKTIME = 5

    __starting_times: Dict[int, str] = {}   # TODO move to new data/CSV-file?
    """ List of starting times - times in which lessons usually starts at FMPH (from 8:10 to 19:00)
        Data format:
            key: time in minutes
            value: time in format H:MM
    """

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
        lessons_sorted_by_days = self.__sort_lessons_by_days()
        self.__set_layout(lessons_sorted_by_days)
        self.__init_last_started_lessons_list()

    def __init_times(self):
        """Fills __starting_times dictionary with data."""
        for minutes in range(self.__TIME_MIN, self.__TIME_MAX, 50):     # TODO some lessons starts in different times (e.g 10:30)
            self.__starting_times[minutes] = self.minutes_2_time(minutes)

    def __init_layout(self): # TODO
        """Initializes layout (2d list)."""
        self.__layout = []
        for i in range(5):
            # pouzivam OrderedDict miesto klasickeho dict, kedze chcem lahko pristupovat k poslednemu vlozenemu prvku:
            od = OrderedDict()
            column = [od]
            self.__layout.append(column)

    def __init_last_started_lessons_list(self):
        """Initializes attribute __last_started_lessons"""
        self.__lessons_in_progress = []
        for di in range(len(self.__layout)):
            self.__lessons_in_progress.append([])
            for ci in range(len(self.__layout[di])):
                self.__lessons_in_progress[di].append(None)

    def __sort_lessons_by_days(self):
        """Sorts all lessons by the days in the week. Each day is a list of lessons."""
        if self.__lessons is None:
            raise Exception("Attribute __lessons cannot be None")
        days: List[List] = []
        for i in range(5):  # 5 dni v tyzdni
            days.append([])
        for lesson in self.__lessons:
            days[lesson.day].append(lesson)
        return days

    def __set_layout(self, lessons_sorted_by_days):
        """ Nastavi layout rozvrhu: vlozi lessons do _layout, tak, ze ich roztriedi podla dni do stlpcov. Kazdy
        stlpec je OrderedDict. Algoritmus sa vzdy snazi pridavat hodiny do co "najviac laveho" stlpca. """

        # Rozdelime hodiny do stlpcov:
        # pre kazdy den v tyzdni
        for i, lessons in enumerate(lessons_sorted_by_days):
            # pre kazdu hodinu v danom dni:
            for lesson in lessons:
                added = False
                # pre kazdy stlpec v danom dni:
                for column in self.__layout[i]:
                    # ak mozes, skus don dat hodinu
                    if self.__can_add_lesson(lesson, column):
                        column[lesson.start] = lesson  #
                        added = True
                        break
                # ak neslo dat, vytvor novy stlpec a vloz ju don
                if not added:
                    new_dict = OrderedDict()
                    new_dict[lesson.start] = lesson
                    self.__layout[i].append(new_dict)

    def __can_add_lesson(self, lesson, column: OrderedDict):
        """Vrati True, ak sa hodina da vlozit do stlpca (neprebieha momentalne ina hodina v danom stlpci).
        Pre spravnu funkcnost musi byt column zoradeny podla casu."""

        if len(column) == 0:
            return True
        if self.__get_last_added_lesson(column).end < lesson.start:
            return True
        return False

    def __get_last_added_lesson(self, column):
        """Vrati lesson, ktora bola naposledy pridana do daneho column."""
        last_lesson_key = next(reversed(column))
        return column[last_lesson_key]


    def get_lessons(self):
        return self.__lessons

    def get_layout(self):
        return self.__layout

    def get_starting_times(self) -> Dict[int, str]:
        return self.__starting_times

    def get_lesson(self, day_index, column_index, time):
        """Vrati hodinu pre dany den, stlpec a cas."""
        lesson = self.__layout[day_index][column_index][time]
        if lesson is None:
            raise Exception("Lesson with these parameters doesn't exists.")
        return lesson

    def start_lesson(self, day_index, column_index, time):
        """zapise ju do __lessons_in_progress"""
        self.__lessons_in_progress[day_index][column_index] = time

    def lesson_in_progress(self, actual_time, day_index, column_index):
        """Vrati True, ak v danom stlpci a danom case prebieha hodina."""
        lesson_key = self.get_lesson_key(day_index, column_index)
        if lesson_key is None:
            return False
        lesson = self.get_lesson(day_index, column_index, lesson_key)

        if lesson is None:
            raise Exception("Lesson cannot be None.")

        if (lesson.start < actual_time) and (lesson.end + lesson.breaktime > actual_time):
            return True
        return False

    def get_lesson_key(self, day_index, column_index):
        """Vrati kluc hodiny do self.__layout (cas), ktora aktualne bezi. Ak taka hodina nebezi, vrati None."""
        return self.__lessons_in_progress[day_index][column_index]

    def get_columns_counts(self) -> Dict:
        """Vrati dict, kde klucom su dni v tyzdni a hodnoty su pocty stlpcov v danych dnoch."""
        result = {}
        for i in range(5):
            result[self.__DAYS[i]] = len(self.__layout[i])
        return result

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
