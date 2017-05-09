import unittest
import datetime
import ujson as json

from betfairlightweight.resources.baseresource import BaseResource
from tests.tools import create_mock_json


class BaseResourceInit(unittest.TestCase):

    def test_init(self):
        base_resource = BaseResource()
        assert base_resource._datetime_created is not None
        assert base_resource._datetime_updated is not None
        assert base_resource.elapsed_time is None
        assert base_resource._data == {}

    def test_data(self):
        mock_response = create_mock_json('tests/resources/base_resource.json')
        base_resource = BaseResource(elapsed_time=1.2,
                                     **mock_response.json())

        assert base_resource.elapsed_time == 1.2
        assert base_resource._data == mock_response.json()

    def test_data_json(self):
        mock_response = create_mock_json('tests/resources/base_resource.json')
        base_resource = BaseResource(elapsed_time=1.2,
                                     **mock_response.json())
        assert base_resource.json() == json.dumps(mock_response.json())

    def test_strip_datetime(self):
        base_resource = BaseResource()
        for string in ['2100-06-01T10:10:00.000Z', '2100-06-01T10:10:00.00Z', '2100-06-01T10:10:00.0Z']:
            stripped = base_resource.strip_datetime(string)
            assert type(stripped) == datetime.datetime

        stripped = base_resource.strip_datetime(None)
        assert not stripped

        stripped = base_resource.strip_datetime('45')
        assert not stripped

        integer = 1465631675000
        stripped = base_resource.strip_datetime(integer)
        assert type(stripped) == datetime.datetime

        stripped = base_resource.strip_datetime(None)
        assert not stripped

        stripped = base_resource.strip_datetime('45')
        assert not stripped

        # stripped = base_resource.strip_datetime(-1230000000345446)
        # assert not stripped  py3.6 is able to strip this

    def test_str_repr(self):
        base_resource = BaseResource()
        assert str(base_resource) == 'BaseResource'
        assert repr(base_resource) == '<BaseResource>'
