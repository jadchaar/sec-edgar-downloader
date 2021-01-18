"""
Tests the initialization of the Downloader object with
relative and absolute download folder paths.
"""

import os
from pathlib import Path

import pytest

from sec_edgar_downloader import Downloader
from sec_edgar_downloader._constants import SUPPORTED_FILINGS


def test_constructor_no_params():
    dl = Downloader()
    expected = Path.cwd()
    assert dl.download_folder == expected


def test_constructor_blank_path():
    dl = Downloader("")
    # pathlib treats blank paths as the current working directory
    expected = Path.cwd()
    assert dl.download_folder == expected


@pytest.mark.skipif(
    os.name == "nt", reason="test should only run on Unix-based systems"
)
def test_constructor_relative_path():
    dl = Downloader("./Downloads")
    expected = Path.cwd() / "Downloads"
    assert dl.download_folder == expected


def test_constructor_user_path():
    dl = Downloader("~/Downloads")
    expected = Path.home() / "Downloads"
    assert dl.download_folder == expected


def test_constructor_custom_path():
    custom_path = Path.home() / "Downloads/SEC/EDGAR/Downloader"
    dl = Downloader(custom_path)
    assert dl.download_folder == custom_path


def test_supported_filings(downloader):
    dl, _ = downloader
    expected = sorted(SUPPORTED_FILINGS)
    assert dl.supported_filings == expected
