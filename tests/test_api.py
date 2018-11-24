""" Tests for API and helpers """
# -*- coding: utf-8 -*-

import sys
import os
import main as api
import helpers
import weather
import responses
from bs4 import BeautifulSoup
import json
import pytest


def get_data_directory():
    """ Returns the absolute path of the data directory """
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'data/'
    )


def load_sample_dialogflow_request():
    """ Loads a sample dialogflow request to a dictionary """
    with open(os.path.join(get_data_directory(), 'sample_dialogflow_request.json')) as req:
        return json.loads(req.read())


def test_can_get_aviation_gov_site():
    """ Tests that the API can retrieve data from aviation.gov """
    test = helpers.get_weather_from_aviation_gov('CYYZ')
    assert test is not None


def test_can_convert_metar_to_dict():
    """ Tests that the api can convert metar raw data to a dictionary """
    metar = open(os.path.join(get_data_directory(), 'metar.txt'),'r').read()
    dictionary = helpers.parse_metar_to_dict(BeautifulSoup(metar, features='html.parser'))
    assert len(dictionary) == 16


def test_can_open_yaml_responses():
    """ Tests the api can open and parse YAML-stored responses """
    yaml_response = helpers.get_response('FlightConditions', 'speech', 'VFR')
    expected = "It's VFR, let's go flying!"
    assert yaml_response == expected


def test_can_parse_icao_code_from_dialogflow():
    """ Tests that the ICAO code can be successfully parsed from a DF request """
    request_dictionary = load_sample_dialogflow_request()
    icao = helpers.get_icao_code_from_dialogflow(request_dictionary)
    assert icao == "CYXU"


def test_can_parse_airport_name_from_dialogflow():
    """ Tests that the ICAO code can be successfully parsed from a DF request """
    request_dictionary = load_sample_dialogflow_request()
    name = helpers.get_airport_name_from_dialogflow(request_dictionary)
    assert name == "London"


def test_end_to_end_api():
    """ Tests the API end-end """

    class RequestTest:
        """ Simple Mock Request Object """

        def get_json(self):
            """ Returns Sample JSON """
            return load_sample_dialogflow_request()
    
    response = api.main(RequestTest())
    error = {
        'fulfillmentText': helpers.get_standard_error_message()
    }
    not_expected = json.dumps(error).lstrip().rstrip()
    clean_response = response.lstrip().rstrip()
    assert clean_response != not_expected


def testget_intent():
    """ Tests the intent can be successfully retrieved"""
    request_dictionary = load_sample_dialogflow_request()
    intent = helpers.get_intent(request_dictionary)
    assert intent == "get_flight_condition"


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


@pytest.mark.skip(reason='not yet complete')
def test_can_get_metar_parsed():
    """ Tests the parsed/read METAR response can be returned """
    metar = open(os.path.join(get_data_directory(), 'metar.txt'),'r').read()
    dictionary = helpers.parse_metar_to_dict(BeautifulSoup(metar, features='html.parser'))
    response = responses.get_metar_parsed(dictionary, 'Test Airport')
    expected = "CYYZ 022100Z 34008KT 1 1/2SM -DZ BR SCT002 OVC004 13/12 A2995 RMK SF3ST5 SLP145"
    assert response == expected
