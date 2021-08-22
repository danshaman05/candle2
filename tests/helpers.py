import urllib.request
from typing import List

from bs4 import BeautifulSoup

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


def get_list_of_elements(url, selector):
    print(url)
    page = get_page(url)
    soup = get_bs_soup(page=page)
    elements = soup.select(selector)
    return [e for e in elements]


def get_href_links_sorted(elements: List):
    return sorted([e['href'] for e in elements])


def get_texts_sorted(elements: List):
    """Return sorted list of texts inside <a> tag elements."""
    return sorted([e.get_text() for e in elements])


def print_elements_count(elements=None, timetable_instance=None, resource_name=None):
    """parameter timetable_instance should be "old" or "new"""
    t_count = len(elements)
    print(f"\n----There are {t_count} {resource_name}s in {timetable_instance} Candle for this test.---")


def print_first_characters(page=None):
    """print out first 300 characters of page"""
    print(page[:300])


def save_page_locally(page=None):
    if page is None:
        raise Exception("response_byte_object cannot be None!")
    with open('candle-saved-page.html', 'w') as f:
        f.write(page)
