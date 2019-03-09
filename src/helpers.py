""" Helpers for all weather methods """
# -*- coding: utf-8 -*-

import os
from ruamel.yaml import YAML
import requests
from bs4 import BeautifulSoup
import logging


def get_standard_error_message():
    """Returns a standard error message

    Returns:
        string -- The standard error message
    """
    return "Sorry, we couldn't get the weather right now, try again soon."


def get_icao_code_from_dialogflow(request_dictionary):
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


def get_airport_name_from_dialogflow(request_dictionary):
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


def get_intent(request_dictionary):
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


def parse_metar_to_dict(aviation_gov_soup):
    """Parses the METAR BS-XML object to a KV dictionary

    Arguments:
        aviation_gov_soup {BeautifulSoupObject} -- Object with METAR info

    Returns:
        dictionary -- Dictionary of values in the metar, or empty dict if none
    """
    metar = aviation_gov_soup.find('metar')
    dictionary = {}
    sky_conditions = []
    for tag in metar:
        if tag.name == 'sky_condition':
            try:
                sky_conditions.append({
                    'cloud_base_ft_agl': tag['cloud_base_ft_agl'],
                    'sky_cover': tag['sky_cover']
                })
            except (TypeError, KeyError):
                pass
        if tag.name and tag.string:
            dictionary[tag.name] = tag.string
    dictionary['sky_conditions'] = sky_conditions
    return dictionary


def get_response(category, speech_or_text='both', key="standard"):
    """Gets a response from the YAML dictionary

    Arguments:
        category {string} -- Category of the response (base of the yaml file)
        speech_or_text {string} -- "speech" or "text" or "both"
        key {string} -- The key of the response (example "IFR")
    """
    responses_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'responses.yaml')
    yaml = YAML()
    with open(responses_path, 'r') as yaml_responses:
        try:
            responses = yaml.load(yaml_responses)
            if speech_or_text == 'both':
                return responses[category][key]['speech'], responses[category][key]['text']
            return responses[category][key][speech_or_text]
        except Exception as exc:
            print(exc)
            logging.error(exc)


def get_weather_from_aviation_gov(icao_code, **kwargs):
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
