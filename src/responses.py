""" Handles the rendering of weather responses to the user """
# -*- coding: utf-8 -*-

import logging
import weather
from helpers import get_standard_error_message, get_response


def get_wind_information(metar_dict, airport):
    """ Returns the current wind information """
    wind_speed, wind_dir = weather.get_wind_information(metar_dict)
    speech, text = get_response('Wind')
    return speech.format(**locals()), text.format(**locals())


def get_visibility(metar_dict, airport):
    """ Returns the current visibility """
    visibility, visibility_km = weather.get_visibility(metar_dict)
    speech, text = get_response('Visibility')
    return speech.format(**locals()), text.format(**locals())


def get_altimeter(metar_dict, airport):
    """ Returns the current altimeter reading """
    alt = weather.get_altimeter(metar_dict)
    speech, text = get_response('Altimeter')
    return speech.format(**locals()), text.format(**locals())


def get_temperature(metar_dict, airport):
    """ Returns the current temperature in celcius and fahrenheit, and dewpoint """
    temp_c, temp_f = weather.get_temperature(metar_dict)
    dew_c, dew_f = weather.get_dewpoint(metar_dict)
    speech, text = get_response('Temperature')
    return speech.format(**locals()), text.format(**locals())


def get_elevation(metar_dict, airport):
    """ Returns the elevation of the aerodrome """
    elevation_m, elevation_f = weather.get_elevation(metar_dict)
    speech, text = get_response('Elevation')
    return speech.format(**locals()), text.format(**locals())


def get_metar_raw(metar_dict, airport):
    """ Returns the raw METAR data """
    raw = weather.get_metar_raw(metar_dict)
    return raw, raw


def get_metar_parsed(metar_dict, airport):
    """ Returns the human-readable version of the METAR """
    spoken = ""
    if 'flight_category' in metar_dict:
        pass
    if 'temp_c' in metar_dict:
        pass


def get_flight_category(metar_dict, airport):
    """Gets the flight category from the metar dictionary"""
    flight_category = weather.get_flight_category(metar_dict)
    try:
        speech, text = get_response('FlightConditions', 'both', flight_category)
        return speech.format(**locals()), text.format(**locals())
    except Exception:
        default = "It's currently {flight_category} at {airport}.".format(**locals())
        return default, default
