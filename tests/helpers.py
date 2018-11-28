""" Helper methods for unit tests """

import os
import json


def get_data_directory():
    """ Returns the absolute path of the data directory """
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'data/'
    )


def load_sample_dialogflow_request():
    """ Loads a sample dialogflow request to a dictionary """
    with open(os.path.join(get_data_directory(), 'sample_dialogflow_request.json')) as req:
        return json.loads(req.read())
