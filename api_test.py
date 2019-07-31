import requests
import pexpect

import pytest

class TestAPI():

    @pytest.fixture(autouse=True)
    def setup(self):
        self.url = 'http://127.0.0.1:5000'

    @pytest.fixture(autouse=True)
    def start_server(self):
        server = pexpect.spawn("python api.py")
        server.expect('Running on '+self.url)
        yield server
        server.kill(9)

    def test_index(self):
        r = requests.get(self.url)
        assert r.status_code == 200

