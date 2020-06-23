#This file contains helper functions
import unidecode

def get_rooms_sorted_by_dashes(rooms_lst) -> dict:
    '''
    Rozdeli mena miestnosti podla pomlcok do dictionary, kde key je vzdy prefix miestnosti (napr. F1-108 ma prefix F1)
    a value su dane pripony ulozene v poli.
    vstup: zoznam objektov triedy models.Room
    vystup: dictionary {string, List stringov}
    '''
    d = dict()
    for room in rooms_lst:
        name = room.name

        # there is one empty string in table room (I don't know why)
        if name == " ":
            continue

        dash_position = name.find('-') # finds first occurence

        if (dash_position) == -1:  # name doesnt contains dash
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

    return d


def get_teachers_sorted_by_family_name(teachers) -> dict:
    ''' Vrati dictionary ucitelov zotriedenych podla zaciatocneho pismena v priezvisku.
    vstup: zoznam objektov triedy models.Teacher zoradenych podla priezviska (family_name)
    vystup: dictionary { string, List objektov Teacher}, kde klucom je zac. pismeno priezviska
    a hodnoty su objekty triedy Teacher'''

    result_dict = {}
    ostatne = []    # specialna kategoria
    for teacher in teachers:
        if teacher.family_name is None or teacher.family_name == '':
            continue

        first_letter = (teacher.family_name[0])     # ziskame prve pismeno family_name (priezviska)
        if first_letter.isalpha() == False:    # niektore mena mozu zacinat na '.', alebo '/', (a pod.), tieto osetrime samostatne v kategorii Ostatne
            ostatne.append(teacher)
            continue
        first_letter = unidecode.unidecode(first_letter)    # zmenime ho na pismeno bez diakritiky (napr. Č zmeni na C)

        if teacher.family_name[:2] == 'Ch':     # family_name zacinajuce na CH je samostatna kategoria.
            first_letter = 'Ch'

        if first_letter not in result_dict:
            result_dict[first_letter] = []
        result_dict[first_letter].append(teacher)

    result_dict['Ostatné'] = ostatne
    return result_dict


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
    return f"{hours}:{minutes}"


def get_short_name(first_name: str, last_name: str):
    '''Vrati skratene meno, napr. pre "Andrej Blaho" vrati "A. Blaho" '''

    if first_name == '':  # Napr. teacher id 1259
        return ''
    return first_name[0] + ". " + last_name
