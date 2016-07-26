from mock import Mock
import json


def create_mock_json(path, status_code=200):
    with open(path) as f:
        resp = Mock()
        resp.content = f.read()
        resp.json.return_value = json.loads(resp.content)
        resp.status_code = status_code
        return resp
