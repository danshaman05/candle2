import pytest


@pytest.fixture()
def url_old():
    """change this URL to match with the old Candle instance"""
    return "https://candle.fmph.uniba.sk/2016-2017-zima"

@pytest.fixture()
def url_new():
    """change this URL to match with the server's URL"""
    return "http://127.0.0.1:5000"

