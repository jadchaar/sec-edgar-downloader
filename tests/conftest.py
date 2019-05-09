import pytest
from shutil import rmtree
from pathlib import Path

@pytest.fixture
def default_download_folder(tmpdir):
    tmp = tmpdir.mkdir("dl")
    yield tmp
    rmtree(tmp)
