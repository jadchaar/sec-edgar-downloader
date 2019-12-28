"""
Tests the initialization of the Downloader object with
relative and absolute download folder paths.
"""

from pathlib import Path

from sec_edgar_downloader import Downloader


def test_constructor_no_params():
    dl = Downloader()
    expected = Path.home().joinpath("Downloads")
    assert dl.download_folder == expected


def test_constructor_blank_path():
    dl = Downloader("")
    # pathlib treats blank paths as the current working directory
    expected = Path.cwd()
    assert dl.download_folder == expected


def test_constructor_relative_path():
    dl = Downloader("./Downloads")
    expected = Path.cwd().joinpath("Downloads")
    assert dl.download_folder == expected


def test_constructor_user_path():
    dl = Downloader("~/Downloads")
    expected = Path.home().joinpath("Downloads")
    assert dl.download_folder == expected


def test_constructor_custom_path():
    custom_path = Path.home().joinpath("Downloads/SEC/EDGAR/Downloader")
    dl = Downloader(custom_path)
    assert dl.download_folder == custom_path
