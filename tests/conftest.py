import pytest
from shutil import rmtree
from pathlib import Path

default_download_folder = str(Path.joinpath(Path.home(), "Downloads", "sec-edgar-filings"))

@pytest.fixture(scope="class", autouse=True)
def clear_download_content():
    rmtree(default_download_folder, ignore_errors=True)
