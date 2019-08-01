import requests
import pexpect
import tempfile
import shutil
import sys

import pytest

class TestAPI():

    @pytest.fixture(autouse=True)
    def setup(self, tmp_dir):
        self.url = 'http://127.0.0.1:5000'
        self.tmp = tmp_dir

    @pytest.fixture()
    def tmp_dir(self):
        tmp = tempfile.mkdtemp(prefix = "pcrud")
        yield tmp
        shutil.rmtree(tmp)

    @pytest.fixture(autouse=True)
    def start_server(self):
        server = pexpect.spawn("python api.py "+self.tmp)
        server.expect('Running on '+self.url)
        yield server
        server.kill(9)

    def test_index(self):
        r = requests.get(self.url)
        assert r.status_code == 200

    def test_post_create(self):
        content_header = {'Content-Type': 'application/json'}
        data = {'name': 'test-file', 'contents':'hello'}
        r = requests.post(self.url+"/files/create", headers=content_header, json=data)

        assert r.status_code == 201
        assert r.text == "File 'test-file' created at '"+self.tmp+"'."

        file_object = open(self.tmp+"/test-file", "r")
        read_content = file_object.read()
        file_object.close()
        assert read_content == "hello"

