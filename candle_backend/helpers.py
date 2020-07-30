#This file contains helper functions

import unidecode
from collections import OrderedDict
from typing import Dict


def get_rooms_sorted_by_dashes(rooms_lst) -> Dict:
    '''
    Rozdeli mena miestnosti podla pomlcok do dictionary, kde key je vzdy prefix miestnosti (napr. F1-108 ma prefix F1)
    a value su dane pripony ulozene v poli.
    vstup: zoznam objektov triedy models.Room
    vystup: dictionary {string, List stringov}
    '''
    d = {}
    for room in rooms_lst:
        name = room.name
        if name == " ":   # v tabulke room mame jednu miestnost s name " "
            continue

        dash_position = name.find('-')
        if (dash_position) == -1:  # name neobsahuje '-'
            prefix = suffix = name
        else:
            prefix = name[0 : dash_position]
            suffix = name[dash_position + 1 : ]

        # ak su data v zlom formate:
        # raise Exception("Bad data format for room. Room must be in format 'prefix-suffix', for example: 'F1-208'")

        #xMieRez je specialny pripad:
        if 'xMieRez' in prefix:
            suffix = prefix
            prefix = "Ostatné"
            if prefix not in d:
                d[prefix] = []
            d[prefix].append(suffix)
        else:
            if prefix not in d:
                d[prefix] = []
            if prefix == suffix:
                d[prefix].append(suffix)
            else:
                d[prefix].append('-'.join([prefix, suffix]))
    return get_ordered_dict(d)


def get_teachers_sorted_by_family_name(teachers) -> Dict:
    ''' Vrati dictionary ucitelov zotriedenych podla zaciatocneho pismena v priezvisku.
    vstup: zoznam objektov triedy models.Teacher zoradenych podla priezviska (family_name)
    vystup: dictionary { string, List objektov Teacher}, kde klucom je zac. pismeno priezviska
    a hodnoty su objekty triedy Teacher'''

    d = {}
    ostatne = []    # specialna kategoria
    for teacher in teachers:
        if teacher.family_name is None or teacher.family_name == '':
            continue

        first_letter = (teacher.family_name[0])     # ziskame prve pismeno family_name (priezviska)
        if first_letter.isalpha() == False:    # niektore mena mozu zacinat na '.', alebo '/', (a pod.), tieto osetrime samostatne v kategorii Ostatne
            ostatne.append(teacher)
            continue
        first_letter = unidecode.unidecode(first_letter)    # zmenime ho na pismeno bez diakritiky (napr. Č zmeni na C)

        if string_starts_with_ch(teacher.family_name):     # family_name zacinajuce na CH je samostatna kategoria.
            first_letter = 'Ch'

        if first_letter not in d:
            d[first_letter] = []
        d[first_letter].append(teacher)

    d['Ostatné'] = ostatne

    return get_ordered_dict(d)


def get_student_groups_sorted_by_first_letter(student_groups) -> dict:
    '''Vrati dictionary kruzkov (student_groups) zotriedenych podla prveho znaku v nazve kruzku.'''
    result_dict = {}
    for group in student_groups:
        first_letter = group.name[0]
        if first_letter not in result_dict:
            result_dict[first_letter] = []
        result_dict[first_letter].append(group)
    return result_dict


def minutes_2_time(time_in_minutes: int) -> str:
    ''' Vrati cas v 24-hodinovom formate.'''
    hours = time_in_minutes // 60
    minutes = time_in_minutes % 60
    return "%d:%02d" % (hours, minutes)




################################

def string_starts_with_ch(prefix : str):
    if prefix.lower()[:2] == "ch":
        return True
    return False


def get_first_letter(input : str) -> str:
    """Napr. pre "F1" vrati "f", pre "Ch1" vrati "ch", pre "Ostatné" vráti "Ostatné\" """

    if input == "Ostatné":
        return "Ostatné"
    elif string_starts_with_ch(input):
        return "ch"
    else:
        return input[0].lower()


def get_ordered_dict(d : Dict) -> OrderedDict:
    'Vrati dict zoradeny podla slovenskej abecedy'

    # TODO dalo by sa optimalizovat - presunut 3 riadky nizsie niekam inam (napr. samostatna trieda)
    alphabet = "a b c d e f g h ch i j k l m n o p q r s t u v w x y z Ostatné"
    alphabet = alphabet.split(' ')
    order: Dict = {i: alphabet.index(i) for i in alphabet}

    sorted_items = sorted(d.items(), key=lambda t: order.get(get_first_letter(t[0])))
    return OrderedDict(sorted_items)