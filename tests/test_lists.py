import pytest

from tests.helpers import print_elements_count, get_list_of_elements, get_href_links_sorted, \
    get_texts_sorted

resources = [
    '/miestnosti',
    '/ucitelia',
    '/kruzky'
]

# A-tag TEXT
@pytest.mark.parametrize("path", resources)
def test_same_a_text(path, url_candle_2016, url_localhost_2016):
    """Both entity lists have same text inside <a> elements."""

    a_tags1 = get_list_of_elements(url=url_candle_2016 + path, selector="#obsah_in li > a")
    a_tags2 = get_list_of_elements(url=url_localhost_2016 + path, selector="#obsah_in li > a")

    texts1: list[str] = get_texts_sorted(a_tags1)
    texts2: list[str] = get_texts_sorted(a_tags2)

    print_elements_count(texts1, "OLD", "a-text")
    print_elements_count(texts2, "NEW", "a-text")

    assert len(texts1) != 0
    assert texts1 == texts2


# A-tag HREF LINK
@pytest.mark.parametrize("path", resources)
def test_same_a_href_links(path, url_candle_2016, url_localhost_2016):
    """Both entity lists have same <a> href links."""

    a_tags1 = get_list_of_elements(url=url_candle_2016 + path, selector="#obsah_in li > a")
    a_tags2 = get_list_of_elements(url=url_localhost_2016 + path, selector="#obsah_in li > a")

    href_links1 = get_href_links_sorted(a_tags1)
    href_links2 = get_href_links_sorted(a_tags2)

    assert len(href_links1) != 0
    assert href_links1 == href_links2


# A-tag ELEMENT
@pytest.mark.parametrize("path", resources)
def test_same_a_elements_in_same_order(path, url_candle_2016, url_localhost_2016):
    """Both entity lists have same <a> elements in same order."""

    a_tags1 = get_list_of_elements(url=url_candle_2016 + path, selector="#obsah_in li > a")
    a_tags2 = get_list_of_elements(url=url_localhost_2016 + path, selector="#obsah_in li > a")

    assert len(a_tags1) != 0
    assert a_tags1 == a_tags2