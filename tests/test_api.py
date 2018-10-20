import sys
import os
sys.path.insert(0, (
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
)
from api import api
from bs4 import BeautifulSoup
import json


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
    test = api._get_weather_from_aviation_gov('CYYZ')
    assert test is not None


def test_can_convert_metar_to_dict():
    """ Tests that the api can convert metar raw data to a dictionary """
    metar = open(os.path.join(get_data_directory(), 'metar.txt'),'r').read()
    dictionary = api._parse_metar_to_dict(BeautifulSoup(metar, features='html.parser'))
    assert len(dictionary) == 16


def test_can_get_flight_category():
    """ Tests that the flight category can be successfully retrieved """
    icao_code = "CYYZ"
    airport_name = "Toronto International Airport"
    bs_data = api._get_weather_from_aviation_gov(icao_code)
    metar_dict = api._parse_metar_to_dict(bs_data)
    print( api._get_flight_category(metar_dict, airport_name) )


def test_can_open_yaml_responses():
    """ Tests the api can open and parse YAML-stored responses """
    yaml_response = api.get_response('FlightConditions', 'speech', 'VFR')
    expected = "It's VFR, let's go flying!"
    assert yaml_response == expected


def test_can_parse_icao_code_from_dialogflow():
    """ Tests that the ICAO code can be successfully parsed from a DF request """
    request_dictionary = load_sample_dialogflow_request()
    icao = api._get_icao_code_from_dialogflow(request_dictionary)
    assert icao == "CYXU"


def test_can_parse_airport_name_from_dialogflow():
    """ Tests that the ICAO code can be successfully parsed from a DF request """
    request_dictionary = load_sample_dialogflow_request()
    name = api._get_airport_name_from_dialogflow(request_dictionary)
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
        'fufillmentText': api.get_standard_error_message()
    }
    assert response != json.dumps(error)