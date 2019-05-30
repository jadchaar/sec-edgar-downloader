.PHONY: auto test clean publish

auto: build36

build36:
	virtualenv venv --python=python3.6
	venv/bin/pip install -r requirements.txt
	venv/bin/pre-commit install

build37:
	virtualenv venv --python=python3.7
	venv/bin/pip install -r requirements.txt
	venv/bin/pre-commit install

build38:
	virtualenv venv --python=python3.8
	venv/bin/pip install -r requirements.txt
	venv/bin/pre-commit install

test:
	rm -f .coverage
	. venv/bin/activate && pytest

lint:
	venv/bin/pre-commit run --all-files

lint-ci:
	venv/bin/pre-commit run --all-files --show-diff-on-failure

clean:
	rm -rf venv .tox .pytest_cache ./**/__pycache__
	rm -rf dist build .egg sec_edgar_downloader.egg-info
	rm -f ./**/*.pyc .coverage

publish: clean
	pip install -U twine wheel
	python3 setup.py sdist bdist_wheel
	twine upload dist/*
	rm -rf dist build .egg sec_edgar_downloader.egg-info
