from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

about = {}
with open("sec_edgar_downloader/_version.py", "r", encoding="utf-8") as f:
    exec(f.read(), about)

setup(
    name="sec-edgar-downloader",
    version=about["__version__"],
    license="MIT",
    author="Jad Chaar",
    author_email="jad.chaar@gmail.com",
    description="Download company filings from the SEC EDGAR database using Python.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/jadchaar/sec-edgar-downloader",
    packages=["sec_edgar_downloader"],
    zip_safe=False,
    install_requires=["lxml>=4.3.4", "requests"],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Financial and Insurance Industry"
        "Natural Language :: English",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Investment"
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    keywords="sec edgar filing financial finance sec.gov",
    project_urls={
        "Bug Reports": "https://github.com/jadchaar/sec-edgar-downloader/issues",
        "Repository": "https://github.com/jadchaar/sec-edgar-downloader",
    },
)
