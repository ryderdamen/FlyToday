import sys
import os
sys.path.insert(0, (
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
)
from api import api
from bs4 import BeautifulSoup


def get_data_directory():
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'data/'
    )


def test_can_get_aviation_gov_site():
    test = api._get_weather_from_aviation_gov('CYYZ')
    assert test is not None


def test_can_convert_metar_to_dict():
    metar = open(os.path.join(get_data_directory(), 'metar.txt'),'r').read()
    dictionary = api._parse_metar_to_dict(BeautifulSoup(metar, features='html.parser'))
    assert len(dictionary) == 16


def test_can_get_flight_category():
    icao_code = "CYYZ"
    airport_name = "Toronto International Airport"
    bs_data = api._get_weather_from_aviation_gov(icao_code)
    metar_dict = api._parse_metar_to_dict(bs_data)
    print( api._get_flight_category(metar_dict, airport_name) )