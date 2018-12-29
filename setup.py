import setuptools
import sys

if sys.version_info < (3, 6):
    raise RuntimeError("This package requires Python 3.6+. Please update your Python environment and try again.")

def parse_readme():
    with open("README.md", "r") as fh:
        long_description = fh.read()
    return long_description

setuptools.setup(
    name="sec_edgar_downloader",
    version="1.1.4",
    license="MIT",
    author="Jad Chaar",
    author_email="jad.chaar@gmail.com",
    description="Python package for downloading company filings (e.g. 8-K, 10-K, 10-Q, 13F, SC 13G, SD) from the SEC EDGAR database.",
    long_description=parse_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/jadchaar/sec-edgar-downloader",
    packages=setuptools.find_packages(),
    install_requires=["beautifulsoup4", "lxml", "requests"],
    package_dir={
        "sec_edgar_downloader": "sec_edgar_downloader"
    },
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=[
        "SEC",
        "EDGAR",
        "Downloader",
        "Filing",
        "sec.gov",
        "8-K",
        "10-K",
        "10-Q",
        "13F",
        "SC 13G",
        "SD",
    ],
)
