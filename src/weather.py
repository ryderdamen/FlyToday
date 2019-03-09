""" All weather-specific information and responses """
# -*- coding: utf-8 -*-

import logging
from helpers import get_standard_error_message, get_response
import dateparser
from datetime import datetime
import timeago


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
    if 'wind_speed_kt' not in metar_dict:
        return None, None
    elif 'wind_dir_degrees' not in metar_dict:
        return None, None
    return metar_dict['wind_speed_kt'], metar_dict['wind_dir_degrees']


def get_visibility(metar_dict):
    """ Returns the current visibility as raw data """
    if 'visibility_statute_mi' not in metar_dict:
        return None, None
    visibility = float(metar_dict['visibility_statute_mi'])
    visibility_km = _convert_stat_miles_to_km(visibility)
    return str(visibility), str(visibility_km)


def get_altimeter(metar_dict):
    """ Returns the current altimeter reading data """
    if 'altim_in_hg' in metar_dict:
        return metar_dict['altim_in_hg']


def get_temperature(metar_dict):
    """ Returns the current temperature in celcius and fahrenheit """
    if 'temp_c' not in metar_dict:
        return None, None
    temp_c = float(metar_dict['temp_c'])
    temp_f = _convert_c_to_f(temp_c)
    return str(temp_c), str(temp_f)


def get_dewpoint(metar_dict):
    """ Returns the current dewpoint in Celcius and Fahrenheit """
    if 'dewpoint_c' not in metar_dict:
        return None, None
    dew_c = float(metar_dict['dewpoint_c'])
    dew_f = _convert_c_to_f(dew_c)
    return str(dew_c), str(dew_f)


def get_elevation(metar_dict):
    """ Returns the elevation of the aerodrome """
    if 'elevation_m' not in metar_dict:
        return None, None
    elevation_m = float(metar_dict['elevation_m'])
    elevation_f = _convert_meters_to_feet(elevation_m)
    return str(elevation_m), str(elevation_f)


def get_metar_raw(metar_dict):
    """ Returns the raw METAR data """
    if 'raw_text' not in metar_dict:
        return None
    return metar_dict['raw_text'].replace('\n', '')


def get_flight_category(metar_dict):
    """Gets the flight category from the metar dictionary"""
    if 'flight_category' not in metar_dict:
        logging.error('flight_category not in metar_dict')
        return None
    flight_category = metar_dict['flight_category'].strip().upper()
    return flight_category


def get_time(metar_dict):
    """ Returns the absolute and relative time of the METAR """
    if 'observation_time' not in metar_dict:
        logging.error('No observation time in metar_dict')
        return None, None
    zulu = dateparser.parse(metar_dict['observation_time']).replace(tzinfo=None)
    now = datetime.utcnow().replace(tzinfo=None)
    relative = timeago.format(zulu, now)
    hours_mins = str(zulu.strftime("%H")) + str(zulu.strftime("%M"))
    return hours_mins, relative


def get_station_id(metar_dict):
    """ Returns the station ID (or None, in an unlikely situation) """
    if 'station_id' in metar_dict:
        return metar_dict['station_id'].upper()


def get_sky_conditions(metar_dict):
    """ Returns list of sky conditions """
    if 'sky_conditions' not in metar_dict:
        return None
    if metar_dict['sky_conditions'] == []:
        return None
    codes = {
        'SKC': 'Clear Skies',
        'FEW': 'Few Clouds',
        'SCT': 'Scattered Clouds',
        'BKN': 'Broken Clouds',
        'OVC': 'Overcast'
    }
    cleaned_conditions = []
    for cond in metar_dict['sky_conditions']:
        if not cond['sky_cover'].upper() in codes:
            cover = cond['sky_cover']
        else:
            cover = codes[cond['sky_cover']]
        cleaned_conditions.append((
            cover, cond['cloud_base_ft_agl']
        ))
    return cleaned_conditions
