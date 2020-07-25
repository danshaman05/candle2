from typing import List, Dict

from candle_backend.models import LessonType

''':
Trieda uchovava timetable a obsahuje funkcie na pracu s nim. 
'''

class Timetable:
    lessons = None
    layout = None   # 3 rozmerny list hodin. Jednotlive urovne su: days->columns->lessons


    def __init__(self, lessons_objects):
        self.set_lessons_list(lessons_objects)


    def set_lessons_list(self, lessons_objects):
        self.lessons = lessons_objects



    # TODO
    # def get_layout(lessons_list: List):      # TODO ZMAZMA;  bolo get_timetable
    #     ''' vrati 3-rozmerne pole hodin predstavujuce rozvrh'''
    #     sorted_lessons_by_days = sort_lessons_by_days(lessons_list)
    #
    #     # zoznam dni - kazdy den je zoznam (list) stlpcov
    #     timetable: List[List[List]] = init_timetable()
    #
    #     # # rozdelime hodiny do stlpcov:
    #     for i, lessons in enumerate(sorted_lessons_by_days):
    #         # pre kazdu hodinu v danom dni:
    #         for lesson in lessons:
    #             added = False
    #             # pre kazdy stlpec v danom dni:
    #             for column in timetable[i]:
    #                 # ak mozes, skus don dat hodinu
    #                 if can_add_lesson(lesson, column):
    #                     column.append(lesson)
    #                     added = True
    #
    #             # ak neslo dat, vytvor novy stlpec a tam ho daj
    #             if (not added):
    #                 timetable[i].append([lesson])
    #
    #     set_lessons_break_times(timetable)
    #
    #     return timetable
    #
    #
    #
    # def format_for_template(lessons_list: List):
    #     '''Naformatuje niektore data do pozadovaneho tvaru pre template.
    #     Nic nevracia. Zmeni lessons_list.'''
    #     for lesson in lessons_list:
    #         lesson['day'] = get_day_abbreviation(lesson['day'])
    #         lesson['start'] = minutes_2_time(lesson['start'])
    #         lesson['end'] = minutes_2_time(lesson['end'])
    #
    #
    #
    #
    # def sort_lessons_by_days(lessons_list: List):
    #     '''Rozdelime hodiny podla dni. Kazdy den bude predstavovat zoznam hodin.'''
    #     sorted_lessons: List[List] = []
    #     for i in range(5):
    #         sorted_lessons.append([])
    #     for lesson in lessons_list:
    #         sorted_lessons[lesson['day']].append(lesson)
    #     return sorted_lessons
    #
    #
    # def init_timetable():
    #     """ Pripravi 3d pole"""
    #     timetable = []
    #     for i in range(5):
    #         timetable.append([[]])
    #     return timetable
    #
    #
    # def can_add_lesson(lesson, column):
    #     ''' Vrati True, ak sa hodina da vlozit do stlpca.
    #     Pre spravnu funkcnost musi byt column zoradeny podla casu.'''
    #     if len(column) == 0:
    #         return True
    #     if column[-1]['end'] < lesson['end']:   # TODO otestovat
    #         return True
    #     return False
    #
    #
    # def set_lessons_break_times(timetable: List[List[List]]):
    #     '''Prejde vsetky lessons v timetable a prida im atribut "breaktime" '''
    #
    #     # toto by sa patrilo niekam vyssie:
    #     shortest_lesson = 45    # najkratsia hodina ma 45 min
    #     shortest_breaktime = 5  # najkratsia prestavka je 5 min
    #
    #     for di in range(5):     # di - day index
    #         for ci in range(len(timetable[di])):    # ci - column index
    #             for lesson in timetable[di][ci]:
    #                 lessons_count = lesson.end - lesson.start / shortest_lesson
    #                 lesson['breaktime'] = lessons_count * shortest_breaktime

