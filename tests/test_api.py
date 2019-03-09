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
from tests.helpers import get_data_directory, load_sample_dialogflow_request


def test_can_get_aviation_gov_site():
    """ Tests that the API can retrieve data from aviation.gov """
    test = helpers.get_weather_from_aviation_gov('CYYZ')
    assert test is not None


def test_can_convert_metar_to_dict():
    """ Tests that the api can convert metar raw data to a dictionary """
    metar = open(os.path.join(get_data_directory(), 'metar.txt'), 'r').read()
    dictionary = helpers.parse_metar_to_dict(BeautifulSoup(metar, features='html.parser'))
    assert len(dictionary) == 17
    assert 'sky_conditions' in dictionary


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
