""" index.py - Fly Today Web Fufillment Handler
    With a specified airport code, retrieves and returns the weather
"""
# -*- coding: utf-8 -*-
import os
import sys
from bs4 import BeautifulSoup
import requests
import json
import yaml
import logging


def _get_standard_error_message():
    """Returns a standard error message
    
    Returns:
        string -- The standard error message
    """
    return "Sorry, we couldn't get the weather right now, try again soon."


def _get_weather_from_aviation_gov(icao_code, **kwargs):
    """Gets weather information from aviation.gov
    
    Arguments:
        icao_code {string} -- the ICAO code as provided by the user
    
    Returns:
        BeautifulSoup Object || None -- Returns a BS Object if successful
    """
    base_url = "https://www.aviationweather.gov/adds/dataserver_current/httpparam"
    parameters = {
        'dataSource': kwargs.get('type', 'metars'),
        'requestType': "retrieve",
        'format': "xml",
        'stationString': icao_code,
        'hoursBeforeNow': kwargs.get('hours', '3'),
        'mostRecent': True,
    }
    response = requests.get(base_url, params=parameters)
    if response.status_code != 200:
        return None
    return BeautifulSoup(response.text, features="html.parser")


def _parse_metar_to_dict(aviation_gov_soup):
    """Parses the METAR BS-XML object to a KV dictionary
    
    Arguments:
        aviation_gov_soup {BeautifulSoupObject} -- Object with METAR info
    
    Returns:
        dictionary -- Dictionary of values in the metar, or empty dict if none
    """
    metar = aviation_gov_soup.find('metar')
    dictionary = {}
    for tag in metar:
        if tag.name and tag.string:
            dictionary[tag.name] = tag.string
    return dictionary


def _get_response(category, speech_or_text, key):
    """Gets a response from the YAML dictionary 
    
    Arguments:
        category {string} -- Category of the response (base of the yaml file)
        speech_or_text {string} -- "speech" or "text"
        key {string} -- The key of the response (example "IFR")
    """
    responses_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'responses.yaml')
    print(responses_path)
    with open(responses_path, 'r') as yaml_responses:
        try:
            responses = yaml.load(yaml_responses)
            return responses[category][key][speech_or_text]
        except yaml.YAMLError as exc:
            print(exc)
            logging.error(exc)


def _get_flight_category(metar_dict, airport):
    """Gets the flight category from the metar dictionary
    
    Arguments:
        metar_dict {dictionary} -- METAR dictionary
        airport {string} -- Full name of the airport
    
    Returns:
        string -- Text response for the user
    """
    if not 'flight_category' in metar_dict:
        return _get_standard_error_message()
    response_dictionary = {
        "LIFR": "It's looking like low IFR right now at {airport}.",
        "IFR": "It's looking like IFR right now at {airport}.",
        "SVFR": "It's looking like special VFR right now at {airport}.",
        "MVFR": "It's looking like marginal VFR right now at {airport}.",
        "VFR": "Good news, it's VFR at {airport}!",
    }
    flight_category = metar_dict['flight_category'].strip().upper()
    if not flight_category in response_dictionary:
        return "It's currently {flight_category} at {airport}.".format(**locals())
    else:
        response = response_dictionary[flight_category]
    return response.format(**locals())


def _get_icao_code_from_dialogflow(request_dictionary):
    """Returns the ICAO code or None from the request dictionary
    
    Arguments:
        request_dictionary {dict} -- The JSON request object from DF as a dictionary
    
    Returns:
        String|None -- The ICAO code string, or None
    """
    try:
        return request_dictionary['queryResult']['parameters']['airport']['ICAO']
    except KeyError as e:
        return None


def _get_airport_name_from_dialogflow(request_dictionary):
    """Returns the airport name or None from the request dictionary
    
     Arguments:
        request_dictionary {dict} -- The JSON request object from DF as a dictionary
    
    Returns:
        String|None -- The airport name string, or None
    """
    try:
        return request_dictionary['queryResult']['parameters']['airport']['name']
    except KeyError as e:
        return None


def _build_text_response(request_json):
    icao_code = _get_icao_code_from_dialogflow(request_json)
    airport_name = _get_airport_name_from_dialogflow(request_json)
    if not icao_code:
        return _get_standard_error_message()
    bs_data = _get_weather_from_aviation_gov(icao_code)
    metar_dict = _parse_metar_to_dict(bs_data)
    return _get_flight_category(metar_dict, airport_name)


def main(request):
    response = _build_text_response(request.get_json())
    return json.dumps({
        'fufillmentText': response
    })
