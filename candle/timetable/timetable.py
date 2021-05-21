from typing import List, Dict
from candle.timetable.placed_lesson import PlacedLesson
from candle.timetable.component import Component


class Timetable:
    """Class represents a timetable."""

    __lessons: List = None
    """list contains objects of model Lesson"""

    __layout: List = None
    """Layout is a three-dimensional list that represents a timetable layout. 
     It is a list of 5 lists - one for every day of the week. Every "day" is a list of "columns". Each column is a list of PlacedLessons.
    (days: List -> columns: List[PlacedLesson])"""


    # teaching times:
    __TIME_MIN = 490    # teaching starts at 8:10 (490 in minutes)
    __TIME_MAX = 1190
    __SHORTEST_LESSON = 45
    __SHORTEST_BREAKTIME = 5

    #  List of starting times - times in which lessons usually starts at FMPH (from 8:10 to 19:00)
    __starting_times: List[str] = []

    __DAYS = "Pondelok, Utorok, Streda, Štvrtok, Piatok".split(',')
    """list of days of the week"""

    # Infolist URL:
    __INFOLIST_URL = 'https://sluzby.fmph.uniba.sk/infolist/SK/'

    def __init__(self, lessons=None):
        """
        :param lessons: Objects of the Lesson model sorted by day and start-time.
        """
        if lessons is None:
            raise Exception("Cannot create timetable without lessons!")
        self.__lessons = lessons
        self.__init_times()
        self.__init_layout()
        self.__set_layout()

    def __init_times(self):
        """Initialize __starting_times list ( starting_times are times when usualy starts lessons at FMFI / FMPH )"""
        self.__starting_times = []
        for minutes in range(self.__TIME_MIN, self.__TIME_MAX, 50):
            self.__starting_times.append(self.minutes_2_time(minutes))

    def __init_layout(self):
        """ Initializes layout as a 2d list (day: List -> column: List )."""
        self.__layout = []
        for i in range(5):
            first_column = []
            self.__layout.append([first_column])

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
            # create a list of components and insert the first component
            components = []
            comp_ind = -1    # component index
            max_component_column = 0
            for lesson in lessons:
                column_index = 0
                while True:
                    if column_index >= 6:
                        raise Exception("Cannot add more than 6 neighbour lessons to one day!")     # TODO flash error message instead of exception & test this code!
                    # if we don't have enough columns:
                    if len(self.__layout[day_index]) - 1 <  column_index:
                        # create a new one and place here lesson:
                        new_column = []
                        self.__layout[day_index].append(new_column)

                    # try to add the lesson:
                    if self.__can_add_lesson(lesson, self.__layout[day_index][column_index]):
                        placed_lesson = PlacedLesson(lesson, column_index)
                        self.__add_neighbours(placed_lesson, day_index)
                        # ak prave ziadna ina hodina nebezi - ide o dalsi komponent:
                        if placed_lesson.has_neigs() == False:
                            # staremu komponentu este nastavme sirku:
                            if len(components) > 0:
                                components[comp_ind].set_width(max_component_column + 1)
                                max_component_column = 0

                            comp_ind += 1
                            components.append(Component())      # create new component

                        self.__layout[day_index][column_index].append(placed_lesson)
                        components[comp_ind].add(placed_lesson)  # add placed_lesson to component
                        # finding the maximum: column used in this component = component width:
                        if placed_lesson.column > max_component_column:
                            max_component_column = placed_lesson.column
                        break
                    column_index += 1

            # set component width for all lessons in the component:
            if components:
                # set width for last component also:
                components[-1].set_width(max_component_column + 1)
                for c in components:
                    c.set_lessons_width()


    def __get_column(self, day_index, column_index):
        return self.__layout[day_index][column_index]

    def __get_ongoing_lesson(self, time, day_index, column_index):
        """Return lesson that is starting, or has already started for the certain time in column. If there is no such lesson,
         return None. Note, that we need to check only last lesson in column."""
        last_lesson = self.__get_last_added_lesson(self.__get_column(day_index, column_index))
        if last_lesson:
            if time >= last_lesson.get_start() and time < last_lesson.get_end():
                return last_lesson
        return None

    def __get_columns_count(self, day_index):
        return len(self.__layout[day_index])

    def __add_neighbours(self, placed_lesson, day_i):
        # left neighbour lessons:
        for col_i in range(placed_lesson.column - 1, -1, -1):
            ongoing_lesson = self.__get_ongoing_lesson(placed_lesson.get_start(), day_i, col_i)
            if ongoing_lesson:
                placed_lesson.add_left_neig(ongoing_lesson)
                ongoing_lesson.add_right_neig(placed_lesson)
                break

        # right neighbour lessons:
        for col_i in range(placed_lesson.column + 1, self.__get_columns_count(day_i)):
            ongoing_lesson = self.__get_ongoing_lesson(placed_lesson.get_start(), day_i, col_i)
            if ongoing_lesson:
                placed_lesson.add_right_neig(ongoing_lesson)
                ongoing_lesson.add_left_neig(placed_lesson)
                break

    # not used now, but maybe later:
    def __get_placed_lessons(self, day_index):
        for column in self.__layout[day_index]:
            for placed_lesson in column:
                yield placed_lesson

    def __can_add_lesson(self, lesson, column: List):
        """ Return True, if there is no ongoing lesson in the column.
        Note, that column has to be sorted by time."""

        # if there is no lesson in the column:
        if len(column) == 0:
            return True
        last_lesson_in_column = self.__get_last_added_lesson(column)
        if last_lesson_in_column.get_end() < int(lesson.start):
            return True
        return False

    def __get_last_added_lesson(self, column):
        """Return the lesson that was added as the last one to the column."""
        if column:
            return column[-1]
        return None


    def get_lessons(self):
        return self.__lessons

    def get_layout(self):
        return self.__layout

    def get_starting_times(self) -> List[str]:
        return self.__starting_times

    def get_days(self):
        """Return list of days in the week."""
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
