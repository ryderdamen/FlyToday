""" index.py - Fly Today Web Fufillment Handler
    With a specified airport code, retrieves and returns the weather
"""
import requests
import json
from bs4 import BeautifulSoup


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


def get_response(type, speech_or_text, key):
    """Gets a response from the YAML dictionary 
    
    Arguments:
        type {[type]} -- [description]
        speech_or_text {[type]} -- [description]
        key {[type]} -- [description]
    """


def _get_flight_category(metar_dict, airport):
    """Gets the flight category from the metar dictionary
    
    Arguments:
        metar_dict {dictionary} -- METAR dictionary
        airport {string} -- Full name of the airport
    
    Returns:
        string -- Text response for the user
    """

    if not 'flight_category' in metar_dict:
        return "Sorry, we couldn't get the weather right now, try again soon."
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


def _build_text_response(request_json):
    icao_code = request_json['queryResult']['parameters']['airport']['ICAO']
    airport_name = request_json['queryResult']['parameters']['airport']['name']
    bs_data = _get_weather_from_aviation_gov(icao_code)
    metar_dict = _parse_metar_to_dict(bs_data)
    return _get_flight_category(metar_dict, airport_name)


def main(request):
    response = _build_text_response(request.get_json())
    return json.dumps({
        'fufillmentText': response
    })