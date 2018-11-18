""" All weather-specific information and responses """
# -*- coding: utf-8 -*-

import logging
from helpers import get_standard_error_message, get_response


def get_wind_information(metar_dict, airport):
    """ Returns the current wind information """
    wind_speed = metar_dict['wind_speed_kt']
    wind_dir = metar_dict['wind_dir_degrees']
    speech, text = get_response('Wind')
    return speech.format(**locals()), text.format(**locals())


def get_visibility(metar_dict, airport):
    """ Returns the current visibility """
    stat_miles_to_km = 1.609344
    visibility = float(metar_dict['visibility_statute_mi'])
    visibility_km = round(visibility * stat_miles_to_km, 1)
    speech, text = get_response('Visibility')
    return speech.format(**locals()), text.format(**locals())


def get_altimeter(metar_dict, airport):
    """ Returns the current altimeter reading """
    alt = metar_dict['altim_in_hg']
    speech, text = get_response('Altimeter')
    return speech.format(**locals()), text.format(**locals())


def get_temperature(metar_dict, airport):
    """ Returns the current temperature in celcius and fahrenheit """
    temp_c = float(metar_dict['temp_c'])
    temp_f = round((1.8 * temp_c) + 32, 1)
    dew_c = float(metar_dict['dewpoint_c'])
    dew_f = round((1.8 * dew_c) + 32, 1)
    speech, text = get_response('Temperature')
    return speech.format(**locals()), text.format(**locals())


def get_elevation(metar_dict, airport):
    """ Returns the elevation of the aerodrome """
    elevation_m = float(metar_dict['elevation_m'])
    elevation_f = round((3.28084 * elevation_m), 1)
    speech, text = get_response('Elevation')
    return speech.format(**locals()), text.format(**locals())


def get_metar_raw(metar_dict, airport):
    """ Returns the raw METAR data """
    raw = metar_dict['raw_text'].replace('\n', '')
    return raw, raw


def get_metar_parsed(metar_dict, airport):
    """ Returns the human-readable version of the METAR """
    pass


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
    flight_category = metar_dict['flight_category'].strip().upper()
    try:
        speech, text = get_response('FlightConditions', 'both', flight_category)
        return speech.format(**locals()), text.format(**locals())
    except Exception:
        default = "It's currently {flight_category} at {airport}.".format(**locals())
        return default, default
