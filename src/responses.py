""" Handles the rendering of weather responses to the user """
# -*- coding: utf-8 -*-

import logging
import weather
from helpers import get_standard_error_message, get_response
import phonetic_alphabet as alpha


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


def replace_point(input_text):
    """ Replaces '.' with 'point' """
    return input_text.replace('.', 'point')


def get_metar_parsed(metar_dict, airport):
    """ Returns the human-readable version of the METAR """
    all_speech = []
    all_text = []

    # Get variables (or None)
    station_id = weather.get_station_id(metar_dict)
    flight_category = weather.get_flight_category(metar_dict)
    wind_speed, wind_dir = weather.get_wind_information(metar_dict)
    visibility, visibility_km = weather.get_visibility(metar_dict)
    altimeter = weather.get_altimeter(metar_dict)
    temp_c, temp_f = weather.get_temperature(metar_dict)
    dew_c, dew_f = weather.get_dewpoint(metar_dict)
    obs_time, relative_time = weather.get_time(metar_dict)
    sky_conditions = weather.get_sky_conditions(metar_dict)

    # Apply Phonetic Alphabet
    station_id_read = alpha.read(station_id).title()
    obs_time_read = alpha.read(obs_time).title()
    wind_speed_read = alpha.read(wind_speed).title()
    wind_dir_read = alpha.read(wind_dir).title()
    visibility_read = replace_point(alpha.read(visibility)).title()
    altimeter_read = replace_point(alpha.read(altimeter)).title()
    temp_c_read = replace_point(alpha.read(temp_c)).title()
    dew_c_read = replace_point(alpha.read(dew_c)).title()

    if station_id:
        all_speech.append(station_id_read + ' - ' + airport.title() + ' Weather.')
        all_text.append(station_id + ' - ' + airport.title() + ' Weather.')
    if obs_time and relative_time:
        speech, text = get_response('Metar', 'both', 'Time')
        all_speech.append(speech.format(**locals()))
        all_text.append(text.format(**locals()))
    if wind_speed and wind_dir:
        speech, text = get_response('Metar', 'both', 'Wind')
        all_speech.append(speech.format(**locals()))
        all_text.append(text.format(**locals()))
    if flight_category:
        speech, text = get_response('Metar', 'both', 'FlightCategory')
        all_speech.append(speech.format(**locals()))
        all_text.append(text.format(**locals()))
    if visibility:
        speech, text = get_response('Metar', 'both', 'Visibility')
        all_speech.append(speech.format(**locals()))
        all_text.append(text.format(**locals()))
    if altimeter:
        speech, text = get_response('Metar', 'both', 'Altimeter')
        all_speech.append(speech.format(**locals()))
        all_text.append(text.format(**locals()))
    if temp_c:
        speech, text = get_response('Metar', 'both', 'Temperature')
        all_speech.append(speech.format(**locals()))
        all_text.append(text.format(**locals()))
    if dew_c:
        speech, text = get_response('Metar', 'both', 'Dewpoint')
        all_speech.append(speech.format(**locals()))
        all_text.append(text.format(**locals()))
    if sky_conditions:
        sc_speech = "Sky Conditions are as follows. "
        sc_text = "Sky Conditions: "
        speech, text = get_response('Metar', 'both', 'SkyCondition')
        for condition, agl in sky_conditions:
            agl_read = alpha.read(agl).title()
            sc_speech += speech.format(**locals()) + ' '
            sc_text += text.format(**locals()) + ' '
        all_speech.append(sc_speech)
        all_text.append(sc_text)
    return ' '.join(all_speech), ' '.join(all_text)


def get_flight_category(metar_dict, airport):
    """Gets the flight category from the metar dictionary"""
    flight_category = weather.get_flight_category(metar_dict)
    try:
        speech, text = get_response('FlightConditions', 'both', flight_category)
        return speech.format(**locals()), text.format(**locals())
    except Exception:
        default = "It's currently {flight_category} at {airport}.".format(**locals())
        return default, default
