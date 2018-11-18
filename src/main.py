""" FlyToday Google Assistant Action Handler"""
# -*- coding: utf-8 -*-

import os
import sys
from bs4 import BeautifulSoup
import requests
import json
import logging
from helpers import (
    get_standard_error_message,
    get_icao_code_from_dialogflow,
    parse_metar_to_dict,
    get_airport_name_from_dialogflow,
    get_intent,
    get_weather_from_aviation_gov
)
from weather import get_metar_raw, get_wind_information, get_flight_category, get_visibility, get_elevation


def build_response(request_json):
    """Builds the response from the request
    
    Arguments:
        request_json {dict} -- The dictionary request object
    
    Returns:
        string -- The string reponse message
    """

    icao_code = get_icao_code_from_dialogflow(request_json)
    airport_name = get_airport_name_from_dialogflow(request_json)
    intent = get_intent(request_json)
    if not icao_code:
        logging.error('No ICAO code provided.')
        return get_standard_error_message()
    
    # Call Aviation.gov
    bs_data = get_weather_from_aviation_gov(icao_code)
    metar_dict = parse_metar_to_dict(bs_data)
    if not metar_dict:
        logging.error("Wasn't able to get metar dictionary.")
        return get_standard_error_message()

    intents = [
        'get_flight_condition',
        'get_wind_speed',
        'get_elevation',
        'get_temperature',
        'get_visibility',
    ]

    # Parse and return intent responses
    if intent == "get_flight_condition":
        return get_flight_category(metar_dict, airport_name)
    elif intent == "get_wind_information":
        return get_wind_information(metar_dict, airport_name)
    elif intent == "get_elevation":
        return get_elevation(metar_dict, airport_name)
    elif intent == "get_visibility":
        return get_visibility(metar_dict, airport_name)
    elif intent == "get_temperature":
        return get_temperature(metar_dict, airport_name)
    if not intent:
        intent = "No Intent"
    logging.error('An unexpected intent occured: ' + intent)
    return get_standard_error_message()


def main(request):
    """Handles the main logic of the webhook
    
    Arguments:
        request {request} -- The request object as provided by GCF
    
    Returns:
        String -- A JSON response
    """
    return json.dumps({
        'fulfillmentText': build_response(request.get_json())
    })
