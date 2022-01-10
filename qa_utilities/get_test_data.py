"""
Utility to create data file for a certain time limit to be used to fetch expeced data for our tests.
"""
import requests
import json
import os

CURRENT_DIR = os.getcwd()
DATA_FILE = '{}/data/data.json'.format(CURRENT_DIR)


def get_data_with_time_limit_and_distmax(date_min=None, date_max=None, dist_max=None):
    """
    runs https://ssd-api.jpl.nasa.gov/cad.api api with mentioned filter conditions to fetch data, formats it and
    writes just the data field of the api response into a json file
    :param date_min: exclude data earlier than this date YYYY-MM-DD or date/time YYYY-MM-DDThh:mm:ss or now for the
    current date
    :param date_max: exclude data later than this date YYYY-MM-DD or date/time YYYY-MM-DDThh:mm:ss or now for the
    current date.
    :param dist_max: exclude data with an approach distance greater than this
    """
    api = "https://ssd-api.jpl.nasa.gov/cad.api?date-min={}&date-max={}&dist-max={}".format(date_min, date_max, dist_max)
    res = requests.get(api)
    assert res.status_code == 200, res.status_code
    data = res.json()
    with open(DATA_FILE, 'w') as f:
        json.dump(data['data'], f)


def main():
    # Remove data file if already exists
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)

    # Create data file: Current extracting the data for all currently known close approaches that have
    # happened or will happen in the 20th and 21st centuries
    get_data_with_time_limit_and_distmax(date_min='1900-01-01', date_max='2100-12-31', dist_max=1)


if __name__ == "__main__":
    main()
