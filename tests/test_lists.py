import urllib.request, urllib.error, urllib.parse

import pytest
from bs4 import BeautifulSoup

@pytest.fixture
def url_old():
    """change this URL to match with the old Candle instance"""
    return "https://candle.fmph.uniba.sk/2016-2017-zima"

@pytest.fixture
def url_new():
    """change this URL to match with the server's URL"""
    return "http://127.0.0.1:5000"


def get_page(url=None):
    """return HTML as string"""
    if url is None:
        raise Exception("URL cannot be None!")
    response = urllib.request.urlopen(url)
    if response.code != 200:
        raise Exception("Response code is not 200!")
    page = response.read().decode("UTF-8")
    return page


def get_bs_soup(page):
    soup = BeautifulSoup(page, 'html.parser')
    return soup


def get_entities(soup=None):
    """Return all entities for the current endpoint.
    Entity is a teacher, room or a student group."""
    assert soup is not None
    # return soup.find("#obsah_in")
    return soup.select("#obsah_in li")


def print_entities_count(entities=None, timetable_instance=None, entity_name=None):
    """parameter timetable_instance should be "old" or "new"""
    t_count = len(entities)
    print(f"\n----There are {t_count} {entity_name} in {timetable_instance} timetable.---")



def entities_count(endpoint, url_old, url_new):
    """Both have same entities count. (E.g. same number of teachers in a list.)"""
    entity = endpoint.strip('/')
    """entity is room, teacher or student-group"""

    # OLD CANDLE
    p1 = get_page(url_old + endpoint)
    s1 = get_bs_soup(p1)
    entities1 = get_entities(s1)
    print_entities_count(entities1, "OLD", entity_name=entity)

    # NEW CANDLE
    p2 = get_page(url_new + endpoint)
    s2 = get_bs_soup(p2)
    entities2 = get_entities(s2)
    print_entities_count(entities2, "NEW", entity_name=entity)

    assert len(entities1) != 0
    assert len(entities1) == len(entities2)


def entities_sets(endpoint, url_old, url_new):
    """Both have same entities."""

    # OLD CANDLE
    p1 = get_page(url_old + endpoint)
    s1 = get_bs_soup(page=p1)
    entities1 = get_entities(soup=s1)

    set1 = set()
    for e in entities1:
        set1.add(e.get_text())

    # NEW CANDLE
    p2 = get_page(url_new + endpoint)
    s2 = get_bs_soup(p2)
    entities2 = get_entities(s2)

    set2 = set()
    for e in entities2:
        set2.add(e.get_text())

    assert set1 == set2



def test_teachers_count(url_old, url_new):
    """Both have same teachers count."""
    entities_count(endpoint='/ucitelia', url_old=url_old, url_new=url_new)


def test_teachers_sets(url_old, url_new):
    """Both have same teachers."""
    entities_sets('/ucitelia', url_old=url_old, url_new=url_new)


def test_rooms_count(url_old, url_new):
    """Both have same rooms count."""
    entities_count('/miestnosti', url_old=url_old, url_new=url_new)


def test_rooms_sets(url_old, url_new):
    """Both have same rooms."""
    entities_sets('/miestnosti', url_old=url_old, url_new=url_new)


def test_groups_count(url_old, url_new):
    """Both have same student-groups count."""
    entities_count('/kruzky', url_old=url_old, url_new=url_new)


def test_groups_sets(url_old, url_new):
    """Both have same student-groups."""
    entities_sets('/kruzky', url_old=url_old, url_new=url_new)



# Others:
def print_first_characters(page):
    """print out first 300 characters of page"""
	print(page[:300])


def save_page_locally(page=None):
    if page is None:
        raise Exception("response_byte_object cannot be None!")
    with open('old_candle_ucitelia.html', 'w') as f:
        f.write(page)
