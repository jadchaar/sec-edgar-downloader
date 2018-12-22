# Cleanup old packages
rm -rf sec_edgar_downloader.egg-info
rm -rf dist
rm -rf build

# Upload package to PyPI
# https://packaging.python.org/tutorials/packaging-projects/
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*