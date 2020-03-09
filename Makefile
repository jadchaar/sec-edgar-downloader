.PHONY: test clean docs publish

build36: PYTHON_VER = python3.6
build37: PYTHON_VER = python3.7
build38: PYTHON_VER = python3.8

build36 build37 build38:
	virtualenv venv --python=$(PYTHON_VER)
	venv/bin/pip install -r requirements.txt
	venv/bin/pre-commit install

test:
	rm -f .coverage coverage.xml
	. venv/bin/activate && pytest

lint:
	venv/bin/pre-commit run --all-files --show-diff-on-failure

clean:
	rm -rf venv .tox .pytest_cache ./**/__pycache__
	rm -rf dist build .egg .eggs sec_edgar_downloader.egg-info
	rm -f ./**/*.pyc .coverage coverage.xml

docs:
	cd docs; make html

publish:
	rm -rf dist build .egg .eggs sec_edgar_downloader.egg-info
	pip3 install -U setuptools twine wheel
	python3 setup.py sdist bdist_wheel
	twine upload dist/*
	rm -rf dist build .egg .eggs sec_edgar_downloader.egg-info
