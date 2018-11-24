""" All weather-specific information and responses """
# -*- coding: utf-8 -*-

import logging
from helpers import get_standard_error_message, get_response


def _convert_c_to_f(temp_c):
    """ Converts celcius to fahrenheit """
    return round((1.8 * temp_c) + 32, 1)


def _convert_stat_miles_to_km(stat_miles):
    """ Converts stat miles to kms """
    stat_miles_to_km = 1.609344
    return round(stat_miles * stat_miles_to_km, 1)


def _convert_meters_to_feet(meters):
    """ Converts meters to feet """
    return round((3.28084 * meters), 1)


def get_wind_information(metar_dict):
    """ Returns the current wind information as raw data """
    wind_speed = metar_dict['wind_speed_kt']
    wind_dir = metar_dict['wind_dir_degrees']
    return wind_speed, wind_dir


def get_visibility(metar_dict):
    """ Returns the current visibility as raw data """
    visibility = float(metar_dict['visibility_statute_mi'])
    visibility_km = _convert_stat_miles_to_km(visibility)
    return visibility, visibility_km


def get_altimeter(metar_dict):
    """ Returns the current altimeter reading data """
    return metar_dict['altim_in_hg']


def get_temperature(metar_dict):
    """ Returns the current temperature in celcius and fahrenheit """
    temp_c = float(metar_dict['temp_c'])
    temp_f = _convert_c_to_f(temp_c)
    dew_c = float(metar_dict['dewpoint_c'])
    dew_f = _convert_c_to_f(dew_c)
    return temp_c, temp_f, dew_c, dew_f


def get_elevation(metar_dict):
    """ Returns the elevation of the aerodrome """
    elevation_m = float(metar_dict['elevation_m'])
    elevation_f = _convert_meters_to_feet(elevation_m)
    return elevation_m, elevation_f


def get_metar_raw(metar_dict):
    """ Returns the raw METAR data """
    return metar_dict['raw_text'].replace('\n', '')


def get_flight_category(metar_dict):
    """Gets the flight category from the metar dictionary"""
    if not 'flight_category' in metar_dict:
        logging.error('flight_category not in metar_dict')
        return None
    flight_category = metar_dict['flight_category'].strip().upper()
    return flight_category
