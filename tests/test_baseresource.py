import unittest
import datetime

from betfairlightweight.resources.baseresource import BaseResource

from tests.tools import create_mock_json


class BaseResourceInit(unittest.TestCase):

    def test_init(self):
        base_resource = BaseResource()
        assert base_resource.Meta.identifier == 'id'
        assert base_resource.Meta.attributes == {'id': 'id'}
        assert base_resource.Meta.sub_resources == {}
        assert base_resource.date_time_sent is None
        assert base_resource.date_time_created is not None
        assert base_resource.elapsed_time is None
        assert base_resource.id is None
        with self.assertRaises(AttributeError):
            assert base_resource.not_in

    def test_data(self):
        mock_response = create_mock_json('tests/resources/base_resource.json')
        base_resource = BaseResource(date_time_sent=datetime.datetime(2003, 8, 4, 12, 30, 45),
                                     **mock_response.json())

        assert base_resource.date_time_sent == datetime.datetime(2003, 8, 4, 12, 30, 45)
        assert base_resource.id == 12345
        assert base_resource.elapsed_time > 0

    def test_data_sub(self):
        mock_response = create_mock_json('tests/resources/base_resource_sub.json')

        class Model(BaseResource):
            class Meta:
                identifier = 'model'
                attributes = {'MainId': 'main_id',
                              'SubId': 'sub_id'}
                sub_resources = {'Id': BaseResource}

        model_response = Model(**mock_response.json())

        assert model_response.main_id == 12345
        assert model_response.id.id == 6789
        assert model_response.sub_id is None

        with self.assertRaises(AttributeError):
            assert model_response.not_in
