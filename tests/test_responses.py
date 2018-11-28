""" Unit Tests for Responses (Depend on responses.yaml strings) """

import os
from tests.helpers import get_data_directory
import helpers
import responses
from bs4 import BeautifulSoup
import pytest


def test_can_get_visibility():
    """ Tests if the visibility response can be successfully returned """
    metar = open(os.path.join(get_data_directory(), 'metar.txt'),'r').read()
    dictionary = helpers.parse_metar_to_dict(BeautifulSoup(metar, features='html.parser'))
    speech, text = responses.get_visibility(dictionary, 'Test Airport')
    expected = "Visibility is looking around 1.5 statute miles (2.4 km)."
    assert speech == expected


def test_can_get_wind_information():
    """ Tests if wind information can be successfully returned """
    metar = open(os.path.join(get_data_directory(), 'metar.txt'),'r').read()
    dictionary = helpers.parse_metar_to_dict(BeautifulSoup(metar, features='html.parser'))
    speech, text = responses.get_wind_information(dictionary, 'Test Airport')
    expected = "At Test Airport, winds are currently 8 knots at 340 degrees."
    assert speech == expected


def test_can_get_temperature():
    """ Tests if temperature information can be successfully returned """
    metar = open(os.path.join(get_data_directory(), 'metar.txt'),'r').read()
    dictionary = helpers.parse_metar_to_dict(BeautifulSoup(metar, features='html.parser'))
    speech, text = responses.get_temperature(dictionary, 'Test Airport')
    expected = "It's currently 13.0 °C (55.4 °F) at Test Airport. The dew point is sitting at  12.0 °C (53.6 °F)"
    assert speech == expected


def test_get_altimiter():
    """ Tests if altimeter info can be successfully returned """
    metar = open(os.path.join(get_data_directory(), 'metar.txt'),'r').read()
    dictionary = helpers.parse_metar_to_dict(BeautifulSoup(metar, features='html.parser'))
    speech, text = responses.get_altimeter(dictionary, 'Test Airport')
    expected = "For Test Airport, you're looking at 29.949802 mmHg."
    assert speech == expected


def test_get_elevation():
    """ Tests if elevation info can be successfully returned """
    metar = open(os.path.join(get_data_directory(), 'metar.txt'),'r').read()
    dictionary = helpers.parse_metar_to_dict(BeautifulSoup(metar, features='html.parser'))
    speech, text = responses.get_elevation(dictionary, 'Test Airport')
    expected = "Elevation for Test Airport is 173.0 meters (567.6 feet) above sea level."
    assert speech == expected


def test_can_get_metar_raw():
    """ Tests the raw METAR response can be returned """
    metar = open(os.path.join(get_data_directory(), 'metar.txt'),'r').read()
    dictionary = helpers.parse_metar_to_dict(BeautifulSoup(metar, features='html.parser'))
    speech, text = responses.get_metar_raw(dictionary, 'Test Airport')
    expected = "CYYZ 022100Z 34008KT 1 1/2SM -DZ BR SCT002 OVC004 13/12 A2995 RMK SF3ST5 SLP145"
    assert speech == expected


def test_get_flight_categories():
    """ Tests the flight_category response can be returned """
    metar = open(os.path.join(get_data_directory(), 'metar.txt'),'r').read()
    dictionary = helpers.parse_metar_to_dict(BeautifulSoup(metar, features='html.parser'))
    speech, text = responses.get_flight_category(dictionary, 'Test Airport')
    expected = "It's looking like low IFR right now at Test Airport."
    assert speech == expected


@pytest.mark.skip('not yet complete')
def test_can_get_metar_parsed():
    """ Tests the parsed/read METAR response can be returned """
    metar = open(os.path.join(get_data_directory(), 'metar.txt'),'r').read()
    dictionary = helpers.parse_metar_to_dict(BeautifulSoup(metar, features='html.parser'))
    speech, text = responses.get_metar_parsed(dictionary, 'Test Airport')
    expected_speech = ""
    expected_text = ""
    print(speech)
    assert speech == expected_speech
    assert text == expected_text

