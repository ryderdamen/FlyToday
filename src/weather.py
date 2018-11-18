""" All weather-specific information and responses """
# -*- coding: utf-8 -*-

import logging
from src.helpers import get_standard_error_message


def get_wind_information(metar_dict, airport):
    wind_speed = metar_dict['wind_speed_kt']
    wind_dir = metar_dict['wind_dir_degrees']
    response = "At {airport}, the wind is currently {wind_speed} knots at {wind_dir} degrees.".format(**locals())
    return response


def get_visibility(metar_dict, airport):
    stat_miles_to_km = 1.609344
    visibility = metar_dict['visibility_statute_mi']
    visibility_km = round(visibility * stat_miles_to_km, 1)
    return "Visibility is looking around {visibility} statute miles ({visibility_km} km)".format(**locals())


def get_altimeter(metar_dict, airport):
    alt = metar_dict['altim_in_hg']
    return "You're looking at {alt} mmHg".format(**locals())


def get_temperature(metar_dict, airport):
    temp = metar_dict['temp_c']
    return "It's currently {temp} degrees Celsius at {airport}".format(**locals())


def get_metar_raw(metar_dict, airport):
    raw = metar_dict['raw_text']
    return raw


def get_flight_category(metar_dict, airport):
    """Gets the flight category from the metar dictionary
    
    Arguments:
        metar_dict {dictionary} -- METAR dictionary
        airport {string} -- Full name of the airport
    
    Returns:
        string -- Text response for the user
    """
    if not 'flight_category' in metar_dict:
        logging.error('flight_category not in metar_dict')
        return get_standard_error_message()
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
