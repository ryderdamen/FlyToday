""" FlyToday Google Assistant Action Handler"""
# -*- coding: utf-8 -*-

import os
import sys
from bs4 import BeautifulSoup
import requests
import json
import logging
import helpers
import weather


def build_response(request_json):
    """Builds the response from the request
    
    Arguments:
        request_json {dict} -- The dictionary request object
    
    Returns:
        string -- The string reponse message
    """

    icao_code = helpers.get_icao_code_from_dialogflow(request_json)
    airport_name = helpers.get_airport_name_from_dialogflow(request_json)
    intent = helpers.get_intent(request_json)
    if not icao_code:
        logging.error('No ICAO code provided.')
        return helpers.get_standard_error_message()
    
    # Call Aviation.gov
    bs_data = helpers.get_weather_from_aviation_gov(icao_code)
    metar_dict = helpers.parse_metar_to_dict(bs_data)
    if not metar_dict:
        logging.error("Wasn't able to get metar dictionary.")
        return helpers.get_standard_error_message()

    intents = [
        'get_flight_condition',
        'get_wind_speed',
        'get_elevation',
        'get_temperature',
        'get_visibility',
    ]

    # Parse and return intent responses
    if intent == "get_flight_condition":
        return weather.get_flight_category(metar_dict, airport_name)
    elif intent == "get_wind_information":
        return weather.get_wind_information(metar_dict, airport_name)
    elif intent == "get_elevation":
        return weather.get_elevation(metar_dict, airport_name)
    elif intent == "get_visibility":
        return weather.get_visibility(metar_dict, airport_name)
    elif intent == "get_temperature":
        return weather.get_temperature(metar_dict, airport_name)
    elif intent == "get_metar_raw":
        return weather.get_metar_raw(metar_dict, airport_name)
    if not intent:
        intent = "No Intent"
    logging.error('An unexpected intent occured: ' + intent)
    return helpers.get_standard_error_message()


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
