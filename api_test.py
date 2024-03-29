import requests
import pexpect
import tempfile
import shutil
import sys
import os.path

import pytest

class TestAPI():

# fixtures
    @pytest.fixture(autouse=True)
    def setup(self, tmp_dir):
        self.url = 'http://127.0.0.1:5000'
        self.tmp = tmp_dir
        self.content_header = {'Content-Type': 'application/json'}

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


# index
    def test_index(self):
        r = requests.get(self.url)
        assert r.status_code == 200
        assert "Actions:" in r.text


# create
    def test_post_create(self):
        data = {'name': 'test-file-to-create', 'contents':'hello'}
        r = requests.post(self.url+"/files/create", headers=self.content_header, json=data)

        assert r.status_code == 201
        assert r.text == "File 'test-file-to-create' created at '"+self.tmp+"'."
        read_content = read_file(self.tmp+"/test-file-to-create")
        assert read_content == "hello"

    def test_post_create_failure_when_file_already_exists(self):
        expected_contents = 'original contents, will not be overwritten'
        write_file(self.tmp+'/test-file-to-create', expected_contents)
        data = {'name': 'test-file-to-create', 'contents':'try to overwrite'}
        r = requests.post(self.url+"/files/create", headers=self.content_header, json=data)

        assert r.status_code == 409
        assert r.text == "File 'test-file-to-create' already exists in '"+self.tmp+"'."
        read_content = read_file(self.tmp+"/test-file-to-create")
        assert read_content == expected_contents


# list
    def test_list_files(self):
        write_file(self.tmp+'/test-file-1', "kitten")
        write_file(self.tmp+'/test-file-2', "puppy")
        r = requests.get(self.url+"/files/read")

        assert r.status_code == 200
        assert r.text == "test-file-1\ntest-file-2"

    def test_list_empty(self):
        r = requests.get(self.url+"/files/read")

        assert r.status_code == 200
        assert r.text == "No files found in "+self.tmp


# read
    def test_get_read(self):
        expected_contents = "contents of the test file"
        write_file(self.tmp+'/test-file-to-read', expected_contents)
        r = requests.get(self.url+"/files/read/test-file-to-read")

        assert r.status_code == 200
        assert r.text == expected_contents

    def test_get_read_fails_when_file_does_not_exist(self):
        r = requests.get(self.url+"/files/read/test-file-to-read")

        assert r.status_code == 404
        assert r.text == "File 'test-file-to-read' not found in '"+self.tmp+"'."


# update
    def test_put_update(self):
        write_file(self.tmp+'/test-file-to-update', 'boring old contents')
        expected_new_contents = 'new shiny updated contents'
        data = {'contents': expected_new_contents}
        r = requests.put(self.url+"/files/update/test-file-to-update", headers=self.content_header, json=data)

        assert r.status_code == 200
        assert r.text == "File 'test-file-to-update' in '"+self.tmp+"' updated."
        read_content = read_file(self.tmp+"/test-file-to-update")
        assert read_content == expected_new_contents

    def test_put_update_failure_when_file_does_not_exist(self):
        data = {'contents': 'new contents, will not be written'}
        r = requests.put(self.url+"/files/update/test-file-to-update", headers=self.content_header, json=data)

        assert r.status_code == 404
        assert r.text == "File 'test-file-to-update' not found in '"+self.tmp+"'."


# delete
    def test_delete_delete(self):
        write_file(self.tmp+'/test-file-to-delete', 'goodbye')
        r = requests.delete(self.url+"/files/delete/test-file-to-delete")

        assert r.status_code == 200
        assert r.text == "File 'test-file-to-delete' deleted from '"+self.tmp+"'."
        assert os.path.exists(self.tmp+'/test-file-to-delete') == False

    def test_delete_delete_fails_when_file_does_not_exist(self):
        r = requests.delete(self.url+"/files/delete/test-file-to-delete")

        assert r.status_code == 404
        assert r.text == "File 'test-file-to-delete' not found in '"+self.tmp+"'."


# helpers
def write_file(filename, contents):
    f = open(filename, "w")
    f.write(contents)
    f.close()

def read_file(filename):
    f = open(filename, "r")
    contents = f.read()
    f.close()
    return contents

