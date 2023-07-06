"""Pytest fixtures for testing suite."""
import shutil

import pytest

from sec_edgar_downloader import Downloader


@pytest.fixture(scope="function")
def downloader(tmp_path):
    dl = Downloader(tmp_path)
    yield dl, tmp_path
    shutil.rmtree(tmp_path)
