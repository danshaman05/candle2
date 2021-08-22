import pytest
from bs4 import NavigableString
from tests.helpers import get_list_of_elements

"""This module tests all lists of lessons in all timetables."""

resources = [
    '/miestnosti',
    '/ucitelia',
    '/kruzky'
]

@pytest.mark.parametrize("path", resources)
def test_timetable_list(path, url_root_localhost_2016, url_root_candle, url_root_localhost):
    """All teachers, rooms and student-groups must have same timetable-list (#rozvrhList in the DOM)."""

    # get links for each timetable from new Candle's list (list of teachers, rooms or student-groups)
    a_tags_new = get_list_of_elements(url=url_root_localhost_2016 + path, selector="#obsah_in li > a")

    # for each link:
    for a in a_tags_new:
        relative_url = a['href']
        #print(url_root_localhost + relative_url)

        # get timetable-list's row:
        tr_elements1 = get_list_of_elements(url=url_root_localhost + relative_url, selector="#rozvrhList > tr")
        tr_elements2 = get_list_of_elements(url=url_root_candle + relative_url, selector="#rozvrhList > tr")

        #Tables must be sorted, otherwise we will get different results:
        assert get_sorted_table_rows(tr_elements1) == get_sorted_table_rows(tr_elements2)


def get_sorted_table_rows(tr_list):
    # return sorted 2d list that represents a timetable-list (#rozvrhList in the DOM).
    lst = []
    for tr in tr_list[1:]:
        lst1 = []
        counter = 0
        for td in tr:
            if isinstance(td, NavigableString):
                continue
            counter += 1
            # We need to skip the list of teachers - they are not sorted in the old Candle,
            #   so we can't test them with 1:1 method:
            if counter == 8:
                continue
            lst1.append(td.text.strip())
        lst.append(lst1)

    """Sort rows (tr elements) by columns: day, start, code, type, note and room."""
    return sorted(lst, key=lambda row: (row[0], row[1], row[5], row[4], row[7], row[3]))
