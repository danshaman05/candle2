from typing import List, Dict, Optional
from _collections import OrderedDict

''':
Trieda uchovava timetable a obsahuje funkcie na pracu s nim. 
'''


class Timetable:
    # zoznam (list) hodin (objekty triedy Lesson)
    __lessons: List = None

    """_layout: 2-rozmerny zoznam (list) hodin usporiadanych pre graficke zobrazenie rozvrhu. 
    Jednotlive urovne su: dni->stlpce. Kazdy stlpec je slovnik (OrderedDict) obsahujuci hodiny ulozene podla kluca (casu), 
    kedy zacinaju v rozvrhu."""
    __layout: List = None

    """2-rozmerny zoznam (list), kt. pre kazdy stlpec uchovava cas hodiny, ktora v nom prave bezi. 
    Dane casy su kluce do __layout."""
    __lessons_in_progress: List[List[Optional[str]]] = None

    # Vyucovacie casy:
    __TIME_MIN = 490
    __TIME_MAX = 1190
    __SHORTEST_LESSON = 45  # najkratsia hodina ma 45 min
    __SHORTEST_BREAKTIME = 5  # najkratsia prestavka je 5 min

    # Zoznam (list) casov, kedy zacinaju hodiny (od 8:10 do 19:00)
    __starting_times: Dict[int, str] = {}

    # Zoznam dni
    __DAYS = "Pondelok, Utorok, Streda, Štvrtok, Piatok".split(',')

    #Infolist URL:
    __INFOLIST_URL = 'https://sluzby.fmph.uniba.sk/infolist/SK/'    # TODO presunut do config.py ?

    def __init__(self, lessons_objects):
        self.__init_times()
        self.__lessons = lessons_objects
        self.__init_layout()
        lessons_sorted_by_days = self.__sort_lessons_by_days()  # usporiadame si hodiny podla dni v tyzdni
        self.__set_layout(lessons_sorted_by_days)
        self.__init_last_started_lessons_list()

    def __init_times(self):
        """
        Zaplni dictionary __times datami - zaciatkami hodin vyucby na FMFI - v tvare:
            kluc: cas v minutach
            hodnota: cas v tvare H:MM
        """
        for minutes in range(self.__TIME_MIN, self.__TIME_MAX, 50):
            self.__starting_times[minutes] = self.minutes_2_time(minutes)

    def __init_layout(self):
        """ Inicializuje 2d list, ktoreho prvky su slovniky (dni -> stlpce -> slovnik)."""

        self.__layout = []
        for i in range(5):
            # pouzivam OrderedDict miesto klasickeho dict, kedze chcem lahko pristupovat k poslednemu vlozenemu prvku:
            od = OrderedDict()
            self.__layout.append([od])

    def __init_last_started_lessons_list(self):
        # Inicializuje atribut __last_started_lessons
        self.__lessons_in_progress = []
        for di in range(len(self.__layout)):
            self.__lessons_in_progress.append([])
            for ci in range(len(self.__layout[di])):
                self.__lessons_in_progress[di].append(None)

    def __sort_lessons_by_days(self):
        """Rozdelime hodiny podla dni v tyzdni. Kazdy den bude predstavovat zoznam hodin."""

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
        ''' Vrati True, ak sa hodina da vlozit do stlpca (neprebieha momentalne ina hodina v danom stlpci).
        Pre spravnu funkcnost musi byt column zoradeny podla casu.'''

        if len(column) == 0:
            return True
        if self.__get_last_added_lesson(column).end < lesson.start:
            return True
        return False

    def __get_last_added_lesson(self, column):
        """Vrati lesson, ktora bola naposledy pridana do daneho column."""
        last_lesson_key = next(reversed(column))
        return column[last_lesson_key]


    def __end_lesson(self, day_index, column_index, lesson_key):
        # Zmaze hodinu z __layout, kedze uz skoncila.
        del self.__layout[day_index][column_index][lesson_key]

    ########################### "Public" metody: ###########################
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
        # zapise ju do __lessons_in_progress
        self.__lessons_in_progress[day_index][column_index] = time

    def lesson_in_progress(self, actual_time, day_index, column_index):
        """Vrati True, ak v danom stlpci a danom case prebieha hodina."""
        lesson_key = self.get_lesson_key(day_index, column_index)
        if lesson_key is None:
            return False
        lesson = self.get_lesson(day_index, column_index, lesson_key)

        if lesson is None:
            raise Exception("Lesson cannot be None.")

        if (lesson.start < actual_time) and (lesson.end + lesson.get_breaktime() > actual_time):
            return True
        return False

    def get_lesson_key(self, day_index, column_index):
        """Vrati kluc hodiny do self.__layout (cas), ktora aktualne bezi. Ak taka hodina nebezi, vrati None."""
        return self.__lessons_in_progress[day_index][column_index]

    def get_columns_count(self) -> Dict:
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
        """ Vrati cas v 24-hodinovom formate."""
        hours = time_in_minutes // 60
        minutes = time_in_minutes % 60
        return "%d:%02d" % (hours, minutes)
