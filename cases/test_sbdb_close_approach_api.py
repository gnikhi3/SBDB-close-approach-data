import pytest
import requests
import json
import enum
from datetime import datetime, timedelta
from qa_utilities.get_test_data import DATA_FILE


class SBDBCloseApproachAPIResponseFields(enum.Enum):
    """Represents the SBDB Close Approach API response fields."""
    des = 0
    orbit_id = 1
    jd = 2
    cd = 3
    dist = 4
    dist_min = 5
    dist_max = 6
    v_rel = 7
    v_inf = 8
    t_sigma_f = 9
    h = 10


class SBDBCloseApproachAPITestCase(object):
    """Class which represents the testcase on SBDB Close Approach API"""

    def __init__(self, **kwargs):
        self.filters = dict()
        # adding default filters of the API
        self.filters['date_min'] = 'now'
        default_date_max = datetime.utcnow() + timedelta(days=60)
        self.filters['date_max'] = default_date_max.strftime('%Y-%m-%d')
        self.filters['dist_max'] = 0.05

        # add filter key value pairs to filter dict
        for key, value in kwargs.items():
            self.filters[key] = value

        # API with filter conditions to be tested
        self.final_api = self.construct_api_based_on_filters()

        # Fields in the API response
        self.expected_fields = [field.name for field in SBDBCloseApproachAPIResponseFields]

    def construct_api_based_on_filters(self):
        """
        Construct API based on the filters, removed default filters and add only remaining filters.
        :return: API string based on the filters
        """

        base_api = 'https://ssd-api.jpl.nasa.gov/cad.api'
        filters = self.filters.copy()

        # Remove default values for API construction
        if self.filters['date_min'] == 'now':
            filters.pop('date_min')
        default_date_max = datetime.utcnow() + timedelta(days=60)
        if self.filters['date_max'] == default_date_max.strftime('%Y-%m-%d'):
            filters.pop('date_max')
        if self.filters['dist_max'] == 0.05:
            filters.pop('dist_max')

        if len(filters) == 1:
            base_api = '{}?{}={}'.format(base_api, list(filters.keys())[0], list(filters.values())[0])

        elif len(filters) > 1:
            base_api = '{}?{}={}'.format(base_api, list(filters.keys())[0], list(filters.values())[0])
            filters.pop(list(filters.keys())[0])
            for filter, value in filters.items():
                base_api = base_api + '&'
                base_api = '{}{}={}'.format(base_api, filter, value)
        api = base_api.replace('_', '-')
        return api

    def get_expected_output(self):
        """
        Read data from data/data.json, filter it based on the self.filters and return the filtered data
        :return: list of filtered data
        """
        f = open(DATA_FILE)
        filtered_data = json.load(f)
        for filter, value in self.filters.items():
            filtered_data = self.filter_data(filtered_data, filter, value)
        return filtered_data

    def filter_data(self, data, key, value):
        """
        :param data: List of data to be filtered
        :param key: filter key can be either of the below values:
            date-min: exclude data earlier than this date YYYY-MM-DD or date/time YYYY-MM-DDThh:mm:ss or now for the current date.
            date-max: exclude data later than this date YYYY-MM-DD or date/tRepresentsime YYYY-MM-DDThh:mm:ss or now for the current date.
            dist-min: exclude data with an approach distance less than this, e.g., 0.05, 10LD (default units: au)
            dist-max: exclude data with an approach distance greater than this (see dist-min)
            min-dist-min: exclude data with an approach minimum-distance less than this, e.g., 0.05, 10LD (default units: au)
            min-dist-max: exclude data with an approach minimum-distance greater than this (see min-dist-min)
            h-min: exclude data from objects with H-values less than this (e.g., 22 meaning objects smaller than this)
            h-max: exclude data from objects with H-value greater than this (e.g., 17.75 meaning objects larger than this)
            v-inf-min: exclude data with V-infinity less than this positive value in km/s (e.g., 18.5)
            v-inf-max: exclude data with V-infinity greater than this positive value in km/s (e.g., 20)
            v-rel-min: exclude data with V-relative less than this positive value in km/s (e.g., 11.2)
            v-rel-max: exclude data with V-relative greater than this positive value in km/s (e.g., 19)
        :param value: Filter value for the filter key based on which filtering happens
        :return: List of filtered data wrt to key and value.
        """
        filtered_data = []
        if key in ['date_min', 'date_max']:
            if value == 'now':
                value = datetime.strftime(datetime.utcnow(), '%Y-%m-%d')
            value = datetime.strptime(value, '%Y-%m-%d')
            if key == 'date_min':
                for row in data:
                    if datetime.strptime(row[SBDBCloseApproachAPIResponseFields.cd.value], '%Y-%b-%d %H:%M') > value:
                        filtered_data.append(row)
            elif key == 'date_max':
                for row in data:
                    if datetime.strptime(row[SBDBCloseApproachAPIResponseFields.cd.value], '%Y-%b-%d %H:%M') < value:
                        filtered_data.append(row)
        elif key == 'dist_min':
            for row in data:
                if float(row[SBDBCloseApproachAPIResponseFields.dist.value]) > float(value):
                    filtered_data.append(row)
        elif key == 'dist_max':
            for row in data:
                if float(row[SBDBCloseApproachAPIResponseFields.dist.value]) < float(value):
                    filtered_data.append(row)
        elif key == 'min_dist_min':
            for row in data:
                if float(row[SBDBCloseApproachAPIResponseFields.dist_min.value]) > float(value):
                    filtered_data.append(row)
        elif key == 'min_dist_max':
            for row in data:
                if float(row[SBDBCloseApproachAPIResponseFields.dist_min.value]) < float(value):
                    filtered_data.append(row)
        elif key == 'h_min':
            for row in data:
                if float(row[SBDBCloseApproachAPIResponseFields.h.value]) > float(value):
                    filtered_data.append(row)
        elif key == 'h_max':
            for row in data:
                if float(row[SBDBCloseApproachAPIResponseFields.h.value]) < float(value):
                    filtered_data.append(row)
        elif key == 'v_inf_min':
            for row in data:
                if float(row[SBDBCloseApproachAPIResponseFields.v_inf.value]) > float(value):
                    filtered_data.append(row)
        elif key == 'v_inf_max':
            for row in data:
                if float(row[SBDBCloseApproachAPIResponseFields.v_inf.value]) < float(value):
                    filtered_data.append(row)
        elif key == 'v_rel_min':
            for row in data:
                if float(row[SBDBCloseApproachAPIResponseFields.v_rel.value]) > float(value):
                    filtered_data.append(row)
        elif key == 'v_rel_max':
            for row in data:
                if float(row[SBDBCloseApproachAPIResponseFields.v_rel.value]) < float(value):
                    filtered_data.append(row)
        # todo: include other filter and limit conditions specified in the API document
        return filtered_data


def cases():
    tests = [
        SBDBCloseApproachAPITestCase(),
        # zero count
        SBDBCloseApproachAPITestCase(dist_max=0),
        SBDBCloseApproachAPITestCase(date_min='now', date_max='2050-01-01'),
        SBDBCloseApproachAPITestCase(date_min='1994-12-01', date_max='2022-01-01', dist_min='0.01'),
        SBDBCloseApproachAPITestCase(v_inf_min='15'),
        SBDBCloseApproachAPITestCase(date_min='2020-12-01', v_inf_min='15.5')
    ]
    # todo: Objects with various filters can be created here to test the API with that particular filter.
    return tests


def get_testnames(param):
    filter_params = param.final_api.split('?')
    if len(filter_params) > 1:
        return filter_params[1]
    else:
        return "no filters"


@pytest.fixture(scope='function', params=cases(), ids=get_testnames)
def get_testcases(request):
    return request.param


class TestSBDBCloseApproachAPI(object):
    def test_sbdb_close_approach_api(self, get_testcases):
        """Test SBDB_close_approach_api with various filter conditions and fetch response. Validate the response
        structure and the response data are as expected."""
        testcase = get_testcases
        res = requests.get(testcase.final_api)
        assert res.status_code == 200, res.status_code
        res_json = res.json()
        expected_output = testcase.get_expected_output()
        assert res_json['signature']['version'] == '1.4', res_json['signature']['version']
        assert int(res_json['count']) == len(expected_output), "Count Mismatch! Count in response: {}, " \
                                                               "\n Expected: {},".format(res_json['count'],
                                                                                         len(expected_output))
        if int(res_json['count']) > 0:
            assert res_json['fields'] == testcase.expected_fields, "Fields Mismatch! Fields in response: {}, " \
                                                                   "\n Expected: {}, ".format(res_json['fields'],
                                                                                              testcase.expected_fields)
            assert res_json['data'] == expected_output, "Data Mismatch! Data in response: {}, " \
                                                        "\n Expected: {},".format(res_json['data'],
                                                                                  expected_output)

    def test_sbdb_close_approach_api_invalid_date_format(self):
        """
        Test SBDB_close_approach_api returns appropriate error message when invalid values are passed to filter
        """
        testcase = SBDBCloseApproachAPITestCase(date_min='2020-Jan-21')
        res = requests.get(testcase.final_api)
        assert res.status_code == 400, res.status_code
        res_json = res.json()
        assert res_json['message'] == "invalid value specified for query parameter 'date-min': " \
                                      "invalid datetime specified (expected 'YYYY-MM-DD', 'YYYY-MM-DDThh:mm:ss', " \
                                      "'YYYY-MM-DD_hh:mm:ss' or 'YYYY-MM-DD hh:mm:ss')", res_json['message']
    # todo: add multiple invalid tests
