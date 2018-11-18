""" index.py - Fly Today Web Fufillment Handler
    With a specified airport code, retrieves and returns the weather
"""
# -*- coding: utf-8 -*-
import os
import sys
from bs4 import BeautifulSoup
import requests
import json
from ruamel.yaml import YAML
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
    yaml = YAML()
    with open(responses_path, 'r') as yaml_responses:
        try:
            responses = yaml.load(yaml_responses)
            return responses[category][key][speech_or_text]
        except Exception as exc:
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
        logging.error('flight_category not in metar_dict')
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


def _get_wind_information(metar_dict, airport):
    wind_speed = metar_dict['wind_speed_kt']
    wind_dir = metar_dict['wind_dir_degrees']
    response = "At {airport}, the wind is currently {wind_speed} knots at {wind_dir} degrees.".format(**locals())
    return response


def _get_visibility(metar_dict, airport):
    stat_miles_to_km = 1.609344
    visibility = metar_dict['visibility_statute_mi']
    visibility_km = round(visibility * stat_miles_to_km, 1)
    return "Visibility is looking around {visibility} statute miles ({visibility_km} km)".format(**locals())


def _get_altimeter(metar_dict, airport):
    alt = metar_dict['altim_in_hg']
    return "You're looking at {alt} mmHg".format(**locals())


def _get_temperature(metar_dict, airport):
    temp = metar_dict['temp_c']
    return "It's currently {temp} degrees Celsius at {airport}".format(**locals())


def _get_metar_raw(metar_dict, airport):
    raw = metar_dict['raw_text']
    return raw


def _get_icao_code_from_dialogflow(request_dictionary):
    """Returns the ICAO code or None from the request dictionary
    
    Arguments:
        request_dictionary {dict} -- The JSON request object from DF as a dictionary
    
    Returns:
        String|None -- The ICAO code string, or None
    """
    try:
        return request_dictionary['queryResult']['parameters']['airport']['ICAO']
    except KeyError:
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
    except KeyError:
        return None


def _get_intent(request_dictionary):
    """Gets the intent of the current conversation
    
    Arguments:
        request_dictionary {dict} -- The JSON request object from DF as a dictionary
    
    Returns:
        String - Intent of the conversation
    """
    try:
        return request_dictionary['queryResult']['intent']['displayName']
    except KeyError:
        return None


def _build_text_response(request_json):
    """Builds the text response from the request
    
    Arguments:
        request_json {dict} -- The dictionary request object
    
    Returns:
        string -- The string reponse message
    """

    icao_code = _get_icao_code_from_dialogflow(request_json)
    airport_name = _get_airport_name_from_dialogflow(request_json)
    intent = _get_intent(request_json)
    if not icao_code:
        logging.error('No ICAO code provided.')
        return _get_standard_error_message()
    
    # Call Aviation.gov
    bs_data = _get_weather_from_aviation_gov(icao_code)
    metar_dict = _parse_metar_to_dict(bs_data)
    if not metar_dict:
        logging.error("Wasn't able to get metar dictionary.")
        return _get_standard_error_message()

    intents = [
        'get_flight_condition',
        'get_wind_speed',
        'get_elevation',
        'get_temperature',
    ]

    # Parse and return intent responses
    if intent == "get_flight_condition":
        return _get_flight_category(metar_dict, airport_name)
    elif intent == "get_wind_speed":
        return _get_flight_category(metar_dict, airport_name)
    elif intent == "get_elevation":
        return _get_flight_category(metar_dict, airport_name)
    if not intent:
        intent = "No Intent"
    logging.error('An unexpected intent occured: ' + intent)
    return _get_standard_error_message()


def main(request):
    """Handles the main logic of the webhook
    
    Arguments:
        request {request} -- The request object as provided by GCF
    
    Returns:
        String -- A JSON response
    """
    return json.dumps({
        'fulfillmentText': _build_text_response(request.get_json())
    })
