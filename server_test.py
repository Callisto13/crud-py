import subprocess

import pytest

class TestAPI():

    def test_server_fails_without_existing_store(self):
        cmd = ["python", "api.py", "dir/does/not/exist"]
        proc = subprocess.Popen(cmd,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
        )
        stdout, stderr = proc.communicate()
        assert proc.returncode == 1
        assert stderr.decode("utf-8") == "The provided store configuration (`dir/does/not/exist`) is not an existing directory.\n"

