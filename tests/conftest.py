import pytest

_url_candle = "https://candle.fmph.uniba.sk"
_url_localhost = "http://127.0.0.1:5000"
_path_2016zima = "/2016-2017-zima"  # remove or edit if testing with newer Candle instance


@pytest.fixture()
def url_candle_2016():
    """Unnecessary unless you test with 2016 Candle instance."""
    return _url_candle + _path_2016zima


@pytest.fixture()
def url_localhost_2016():
    """Unnecessary unless you test with 2016 Candle instance."""
    return _url_localhost + _path_2016zima


@pytest.fixture()
def url_candle():
    return _url_candle

@pytest.fixture()
def url_localhost():
    return _url_localhost