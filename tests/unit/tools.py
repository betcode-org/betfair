from unittest import mock
import json


def create_mock_json(path, status_code=200):
    with open(path) as f:
        resp = mock.Mock()
        resp.content = resp.text = f.read().encode("utf-8")
        resp.json.return_value = json.loads(resp.content)
        resp.status_code = status_code
        return resp
