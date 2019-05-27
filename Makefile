.PHONY: auto test clean publish

auto: build36

build36:
	virtualenv local --python=python3.6
	local/bin/pip install -r requirements.txt
	local/bin/pre-commit install

build37:
	virtualenv local --python=python3.7
	local/bin/pip install -r requirements.txt
	local/bin/pre-commit install

build38:
	virtualenv local --python=python3.8
	local/bin/pip install -r requirements.txt
	local/bin/pre-commit install

test:
	rm -f .coverage
	. local/bin/activate && pytest

lint:
	local/bin/pre-commit run --all-files

lint-ci:
	local/bin/pre-commit run --all-files --show-diff-on-failure

clean:
	rm -rf local .pytest_cache ./**/__pycache__
	rm -rf dist build .egg sec_edgar_downloader.egg-info
	rm -f ./**/*.pyc .coverage

publish: clean
	pip install -U twine wheel
	python3 setup.py sdist bdist_wheel
	twine upload dist/*
	rm -rf dist build .egg sec_edgar_downloader.egg-info
