""" Tato singleton trieda sluzi na manazovanie rozvrhov (duplikovanie, ziskanie unikatneho nazvu, mazanie, atd ). """
#### AKO SINGLETON:
from typing import Tuple
from timetable.EditableTimetable import EditableTimetable



class EditableTimetableManager:
    """Inspirovane Singleton patternom: https://stackabuse.com/the-singleton-design-pattern-in-python/"""
    __instance__ = None

    def __init__(self):
        if EditableTimetableManager.__instance__ is None:
            EditableTimetableManager.__instance__ = self
            self.__timetables = {}      # TODO OrderedDict ?
        else:
            raise Exception("You cannot create another EditableTimetableManager class")

    @staticmethod
    def get_instance():
        """ Static method to fetch the current instance."""
        if not EditableTimetableManager.__instance__:
            print("VYTVARAM NOVU INSTANCIU ETM")
            EditableTimetableManager()
        return EditableTimetableManager.__instance__


    # def __init__(self, user):
    #     print("VYTVARAM NOVU INSTANCIU ETM")
    #     self.__timetables = {}
    #     self.set_timetables(user)

    def set_timetables(self, user):
        """ Vlozi userove rozvrhy do __timetables (dictionary).
        Klucom su id-cka, ktore budu v URL daneho rozvrhu (nejde o id z databazy!)"""
        # nacitame userove rozvhry:
        for i, t in enumerate(user.timetables):
            et = EditableTimetable(t)
            et.set_key(i)
            self.__timetables[i] = et

    def get_timetables_count(self):
        return len(self.__timetables)

    def get_max_key(self):
        """Vrati identifikator (key) posledne pridaneho rozvrhu"""
        if len(self.__timetables) == 0:
            return 0
        keys_list = sorted(self.__timetables.keys())
        print("vraciam max_key: " + str(keys_list[-1]))
        return keys_list[-1]

    def get_next_key(self):
        return self.get_max_key() + 1

    def get_timetables(self):
        # TODO zrejme by mal vracat vzdy v rovnakom poradi (zaruci OrderedDict)
        return self.__timetables

    def is_not_empty(self):
        return self.get_timetables_count() != 0

    def get_first_timetable(self) -> Tuple:
        """Metoda vrati prvy rozvrh."""
        id1 = sorted(self.__timetables.keys())[0]
        return self.__timetables[id1], id1

    def get_timetable(self, key):
        return self.__timetables[int(key)]

    def delete_timetable(self, key):
        del self.__timetables[key]