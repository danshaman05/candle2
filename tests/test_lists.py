from typing import List

import pytest

from tests.helpers import get_page, get_bs_soup, print_elements_count

resources = [
    '/miestnosti',
    '/ucitelia',
    '/kruzky'
]

# A-tag TEXT
@pytest.mark.parametrize("path", resources)
def test_same_a_text(path, url_old_2016, url_new_2016):
    """E.g.: both list of teachers rooms, etc have same text inside <a> elements."""
    elements1 = get_list_of_elements(url=url_old_2016 + path, selector="#obsah_in li > a")
    elements2 = get_list_of_elements(url=url_new_2016 + path, selector="#obsah_in li > a")

    texts1: list[str] = get_texts_sorted(elements1)
    texts2: list[str] = get_texts_sorted(elements2)

    print_elements_count(texts1, "OLD", "a-text")
    print_elements_count(texts2, "NEW", "a-text")

    assert len(texts1) != 0
    assert texts1 == texts2


#A-tag HREF LINK
@pytest.mark.parametrize("path", resources)
def test_same_a_href_links(path, url_old_2016, url_new_2016):
    """E.g.: both list of teachers (or rooms, etc) have same <a> href links."""

    elements1 = get_list_of_elements(url=url_old_2016 + path, selector="#obsah_in li > a")
    elements2 = get_list_of_elements(url=url_new_2016 + path, selector="#obsah_in li > a")

    href_links1 = get_href_links_sorted(elements1)
    href_links2 = get_href_links_sorted(elements2)

    assert len(href_links1) != 0
    assert href_links1 == href_links2


# A-tag ELEMENT
@pytest.mark.parametrize("path", resources)
def test_same_a_elements(path, url_old_2016, url_new_2016):
    """E.g.: both list of teachers (or rooms, etc.) have same <a> elements."""

    list1 = get_list_of_elements(url=url_old_2016 + path, selector="#obsah_in li > a")
    list2 = get_list_of_elements(url=url_new_2016 + path, selector="#obsah_in li > a")

    assert len(list1) != 0
    assert list1 == list2



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
