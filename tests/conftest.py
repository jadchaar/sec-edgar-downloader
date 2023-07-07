"""Pytest fixtures for testing suite."""
import shutil

import pytest

from sec_edgar_downloader import Downloader

COMPANY_NAME = "SEC Edgar Downloader Tests"
EMAIL = "foo@bar.com"


@pytest.fixture(scope="function")
def downloader(tmp_path):
    dl = Downloader(COMPANY_NAME, EMAIL, tmp_path)
    yield dl, tmp_path
    shutil.rmtree(tmp_path)
