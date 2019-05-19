from setuptools import setup

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="sec-edgar-downloader",
    version="2.0.1",
    license="MIT",
    author="Jad Chaar",
    author_email="jad.chaar@gmail.com",
    description="Python package for downloading company filings from the SEC EDGAR database.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/jadchaar/sec-edgar-downloader",
    packages=["sec_edgar_downloader"],
    zip_safe=False,
    install_requires=["beautifulsoup4", "lxml", "requests"],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="sec edgar downloader filing financial finance sec.gov 8-k 10-k 10-q 13f 13f-nt 13f-hr sc-13g sd",
    project_urls={
        "Bug Reports": "https://github.com/jadchaar/sec-edgar-downloader/issues",
        "Source": "https://github.com/jadchaar/sec-edgar-downloader",
    },
)
