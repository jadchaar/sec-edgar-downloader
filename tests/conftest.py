"""Pytest fixtures for testing suite."""


import shutil

import pytest

from sec_edgar_downloader import Downloader


@pytest.fixture(scope="function")
def downloader(tmp_path):
    tmp_dir = tmp_path / "Downloads"
    tmp_dir.mkdir()
    dl = Downloader(tmp_dir)
    yield dl, tmp_dir
    shutil.rmtree(tmp_dir)
