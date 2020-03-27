"This file contains helper functions"

'''
Rozdeli mena miestnosti podla pomlcok do dictionary, kde key je vzdy prefix miestnosti (napr. F1-108 ma prefix F1)
a value su dane pripony ulozene v poli.
vstup:
vystup: dictionary <str, list of str>
'''
def getRoomsSortedByDashes_dict(rooms_lst) -> dict:
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