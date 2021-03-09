from unittest import mock
import json


def create_mock_json(path, status_code=200):
    with open(path) as f:
        resp = mock.Mock()
        _data = f.read()
        resp.text = _data
        resp.content = _data.encode("utf-8")
        resp.json.return_value = json.loads(_data)
        resp.status_code = status_code
        return resp
