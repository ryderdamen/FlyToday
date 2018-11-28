""" FlyToday Google Assistant Action Handler"""
# -*- coding: utf-8 -*-

import os
import sys
from bs4 import BeautifulSoup
import requests
import json
import logging
import helpers
import responses


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
        return helpers.get_standard_error_message(), helpers.get_standard_error_message()
    
    # Call Aviation.gov
    bs_data = helpers.get_weather_from_aviation_gov(icao_code)
    metar_dict = helpers.parse_metar_to_dict(bs_data)
    if not metar_dict:
        logging.error("Wasn't able to get metar dictionary.")
        return helpers.get_standard_error_message(), helpers.get_standard_error_message()

    intents = {
        'get_flight_condition': responses.get_flight_category,
        'get_wind_information': responses.get_wind_information,
        'get_elevation': responses.get_elevation,
        'get_visibility': responses.get_visibility,
        'get_temperature': responses.get_temperature,
        'get_metar_raw': responses.get_metar_raw,
        'get_altimeter': responses.get_altimeter,
    }

    if intent not in intents:
        logging.error('An unexpected intent occured: ' + intent)
        return helpers.get_standard_error_message(), helpers.get_standard_error_message()
    
    return intents[intent](metar_dict, airport_name)


def main(request):
    """Handles the main logic of the webhook
    
    Arguments:
        request {request} -- The request object as provided by GCF
    
    Returns:
        String -- A JSON response
    """
    speech, text = build_response(request.get_json())
    return json.dumps({
        'fulfillmentText': speech
    })
