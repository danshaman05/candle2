import pytest

_url_candle = "https://candle.fmph.uniba.sk"
_url_localhost = "http://127.0.0.1:5000"
_path_2016zima = "/2016-2017-zima"



@pytest.fixture()
def url_old_2016():
    """change this URL to match with the old Candle instance"""
    return _url_candle + _path_2016zima


@pytest.fixture()
def url_new_2016():
    """change this URL to match with the server's URL"""
    return _url_localhost + _path_2016zima


# @pytest.fixture()
# def url_candle():
#     return "https://candle.fmph.uniba.sk"