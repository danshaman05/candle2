from typing import Tuple


# def get_timetables():
#     return self.__timetables


def get_timetable(self, key):
    return self.__timetables[int(key)]

def delete_timetable(self, key):
    del self.__timetables[key]

#
# def get_max_timetable_id():
#     return UserTimetable.query