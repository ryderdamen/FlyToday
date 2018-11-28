""" Tests for the weather module """

import os
import weather
import helpers
from tests.helpers import get_data_directory
from bs4 import BeautifulSoup


metar = open(os.path.join(get_data_directory(), 'metar.txt'),'r').read()
metar_dict = helpers.parse_metar_to_dict(BeautifulSoup(metar, features='html.parser'))


def test_get_wind_information():
    speed, direction = weather.get_wind_information(metar_dict)
    assert speed == '8'
    assert direction == '340'


def test_when_no_wind_direction_return_none():
    temp_dict = metar_dict
    del temp_dict['wind_dir_degrees']
    speed, direction = weather.get_wind_information(temp_dict)
    assert speed is None
    assert direction is None


def test_when_no_wind_speed_return_none():
    temp_dict = metar_dict
    del temp_dict['wind_speed_kt']
    speed, direction = weather.get_wind_information(temp_dict)
    assert speed is None
    assert direction is None


def test_get_visibility():
    vis, vis_km = weather.get_visibility(metar_dict)
    assert vis == '1.5'
    assert vis_km == '2.4'
    

def test_when_no_visibility_return_none():
    temp_dict = metar_dict
    del temp_dict['visibility_statute_mi']
    vis, vis_km = weather.get_visibility(temp_dict)
    assert vis is None
    assert vis_km is None


def test_get_altimeter():
    alt = weather.get_altimeter(metar_dict)
    assert alt == '29.949802'


def test_when_no_alt_return_none():
    temp_dict = metar_dict
    del temp_dict['altim_in_hg']
    alt = weather.get_altimeter(temp_dict)
    assert alt is None


def test_get_temperature():
    temp_c, temp_f = weather.get_temperature(metar_dict)
    assert temp_c == '13.0'
    assert temp_f == '55.4'


def test_when_no_temp_return_none():
    temp_dict = metar_dict
    del temp_dict['temp_c']
    temp_c, temp_f = weather.get_temperature(temp_dict)
    assert temp_c is None
    assert temp_f is None


def test_get_dewpoint():
    dew_c, dew_f = weather.get_dewpoint(metar_dict)
    assert dew_c == '12.0'
    assert dew_f == '53.6'


def test_when_no_dewpoint_return_none():
    temp_dict = metar_dict
    del temp_dict['dewpoint_c']
    dew_c, dew_f = weather.get_dewpoint(temp_dict)
    assert dew_c is None
    assert dew_f is None


def test_get_elevation():
    elevation_m, elevation_f = weather.get_elevation(metar_dict)
    assert elevation_m == '173.0'
    assert elevation_f == '567.6'


def test_when_no_elevation_return_none():
    temp_dict = metar_dict
    del temp_dict['elevation_m']
    elevation_m, elevation_f = weather.get_elevation(temp_dict)
    assert elevation_m is None
    assert elevation_f is None


def test_get_metar_raw():
    raw = weather.get_metar_raw(metar_dict)
    expected = 'CYYZ 022100Z 34008KT 1 1/2SM -DZ BR SCT002 OVC004 13/12 A2995 RMK SF3ST5 SLP145'
    assert raw == expected


def test_when_no_metar_raw_return_none():
    temp_dict = metar_dict
    del temp_dict['raw_text']
    assert weather.get_metar_raw(temp_dict) is None


def test_get_flight_category():
    cat = weather.get_flight_category(metar_dict)
    assert cat == 'LIFR'


def test_when_flight_category_is_weird_return_weird():
    temp_dict = metar_dict
    temp_dict['flight_category'] = 'WEIRD'
    cat = weather.get_flight_category(temp_dict)
    assert cat == 'WEIRD'


def test_when_no_flight_category_return_none():
    temp_dict = metar_dict
    del temp_dict['flight_category']
    cat = weather.get_flight_category(temp_dict)
    assert cat is None


def test_get_time():
    zulu, relative = weather.get_time(metar_dict)
    assert zulu == '2100'
    assert type(relative) == str


def test_when_no_time_return_none():
    temp_dict = metar_dict
    del temp_dict['observation_time']
    zulu, relative = weather.get_time(temp_dict)
    assert zulu is None
    assert relative is None


def test_get_station_id():
    the_id = weather.get_station_id(metar_dict)
    assert the_id == 'CYYZ'


def test_when_no_station_id_return_none():
    temp_dict = metar_dict
    del temp_dict['station_id']
    the_id = weather.get_station_id(temp_dict)
    assert the_id is None


def test_get_sky_conditions():
    conditions = weather.get_sky_conditions(metar_dict)
    assert conditions[0][0] == 'Scattered Clouds'
    assert conditions[0][1] == '200'
    assert conditions[1][0] == 'Overcast'
    assert conditions[1][1] == '400'


def test_when_empty_sky_conditions_return_none():
    """ Returns None, not just empty array """
    temp_dict = metar_dict
    temp_dict['sky_conditions'] = []
    assert weather.get_sky_conditions(temp_dict) is None


def test_when_no_sky_conditions_return_none():
    """ Returns None, not just empty array """
    temp_dict = metar_dict
    del temp_dict['sky_conditions']
    assert weather.get_sky_conditions(temp_dict) is None


def test_when_weird_sky_condition_return_weird():
    temp_dict = metar_dict
    new_sky_conditions = [{
        'cloud_base_ft_agl': '500',
        'sky_cover': 'WEIRD'
    }]
    temp_dict['sky_conditions'] = new_sky_conditions
    conditions = weather.get_sky_conditions(metar_dict)
    assert conditions[0][0] == 'WEIRD'
    assert conditions[0][1] == '500'
