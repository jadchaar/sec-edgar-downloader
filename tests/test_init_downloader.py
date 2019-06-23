"""Tests the initialization of the Downloader object with
relative and absolute download folder paths.
"""

from pathlib import Path

from sec_edgar_downloader import Downloader


def test_constructor_no_params():
    dl = Downloader()
    assert str(dl._download_folder) == str(Path.home().joinpath("Downloads"))


def test_constructor_blank_path():
    dl = Downloader("")
    # pathlib treats blank paths as the current working directory
    assert str(dl._download_folder) == str(Path.cwd())


def test_constructor_relative_path():
    dl = Downloader("./Downloads")
    assert str(dl._download_folder) == str(Path.cwd().joinpath("Downloads"))


def test_constructor_user_path():
    dl = Downloader("~/Downloads")
    assert str(dl._download_folder) == str(Path.home().joinpath("Downloads"))


def test_constructor_custom_path():
    custom_path = Path.home().joinpath("Downloads/SEC/EDGAR/Downloader")
    dl = Downloader(custom_path)
    assert str(dl._download_folder) == str(custom_path)
