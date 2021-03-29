from typing import List, Dict, Optional
from _collections import OrderedDict

from .PlacedLesson import PlacedLesson


class Timetable:
    ''' This class represents a timetable. '''

    __lessons: List = None  # list contains objects of model Lesson

    """_layout: 2-rozmerny zoznam (list) hodin usporiadanych pre graficke zobrazenie rozvrhu. 
    Jednotlive urovne su: dni->stlpce. Kazdy stlpec je slovnik (OrderedDict) obsahujuci hodiny ulozene podla kluca (casu), 
    kedy zacinaju v rozvrhu."""
    __layout: List = None

    """2-rozmerny zoznam (list), kt. pre kazdy stlpec uchovava cas hodiny, ktora v nom prave bezi. 
    Dane casy su kluce do __layout."""
    __lessons_in_progress: List[List[Optional[str]]] = None

    # teaching times:
    __TIME_MIN = 490    # teaching starts at 8:10 (490 in minutes)
    __TIME_MAX = 1190
    __SHORTEST_LESSON = 45
    __SHORTEST_BREAKTIME = 5

    # List of starting times (from 8:10 to 19:00)
    __starting_times: List[str] = []

    # list of days of the week
    __DAYS = "Pondelok, Utorok, Streda, Štvrtok, Piatok".split(',')

    # Infolist URL:
    __INFOLIST_URL = 'https://sluzby.fmph.uniba.sk/infolist/SK/'    # TODO presunut do config.py ?

    def __init__(self, lessons_objects):
        self.__init_times()
        self.__lessons = lessons_objects
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
        """ Initializes 2d list which contains OrderedDict-s (days -> columns -> OrderedDict)."""
        self.__layout = []
        for i in range(5):
            # I use OrderedDict instead of normal dict, because I want to easily access a last added element:
            od = OrderedDict()  # TODO: Maybe we should go only with lists...
            self.__layout.append([od])


    def __get_lessons_sorted_by_days(self):
        """Vrati hodiny rozdelene do dni. Rozdelime hodiny podla dni v tyzdni. Kazdy den bude predstavovat zoznam hodin."""

        if self.__lessons is None:
            raise Exception("Attribute __lessons cannot be None")

        days: List[List] = []
        for i in range(5):  # 5 dni v tyzdni
            days.append([])
        for lesson in self.__lessons:
            days[lesson.day].append(lesson)
        return days

    def __set_layout(self):
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
                        raise Exception("Cannot add more than 6 neighbour lessons in one day!") # TODO test it!
                    # if we don't have enough columns, create a new one:
                    if len(self.__layout[day_index]) - 1 <  column_index:
                        new_dict = OrderedDict()
                        self.__layout[day_index].append(new_dict)
                    # try to add the lesson:
                    if self.__can_add_lesson(lesson, self.__layout[day_index][column_index]):
                        self.__layout[day_index][column_index][lesson.start] = PlacedLesson(lesson, column_index)
                        break
                    column_index += 1


    def __can_add_lesson(self, lesson, column: OrderedDict) -> bool:
        ''' Vrati True, ak sa hodina da vlozit do stlpca (neprebieha momentalne ina hodina v danom stlpci).
        Pre spravnu funkcnost musi byt column zoradeny podla casu.'''
        if len(column) == 0:
            return True
        if self.__get_last_added_lesson(column).get_end() < int(lesson.start):
            return True
        return False

    def __get_last_added_lesson(self, column):
        """Vrati lesson, ktora bola naposledy pridana do daneho column."""
        last_lesson_key = next(reversed(column))
        return column[last_lesson_key]




    ########################### "Public" metody: ###########################
    def get_lessons(self):
        return self.__lessons

    def get_layout(self):
        return self.__layout

    # def get_starting_times(self) -> Dict[int, str]:
    #     return self.__starting_times

    def get_starting_times(self) -> List[str]:
        return self.__starting_times

    def get_days(self):
        """Returns list of days in the week."""
        return self.__DAYS


    ########################### Class methods: ###########################
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
        """ Vrati cas v 24-hodinovom formate."""
        hours = time_in_minutes // 60
        minutes = time_in_minutes % 60
        return "%d:%02d" % (hours, minutes)
