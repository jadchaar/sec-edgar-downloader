.PHONY: auto test lint clean cleanbuild publish

auto: build37

build36:
	virtualenv env --python=python3.6
	env/bin/pip install -r requirements.txt

build37:
	virtualenv env --python=python3.7
	env/bin/pip install -r requirements.txt

test:
	rm -f .coverage
	. env/bin/activate && pytest --cov-config=setup.cfg --cov=sec_edgar_downloader tests

lint:
	env/bin/flake8 --config=setup.cfg sec_edgar_downloader tests

clean:
	rm -rf env .pytest_cache ./**/__pycache__
	rm -f ./**/*.pyc .coverage

publish: clean build37
	pip install -U twine
	env/bin/python3 setup.py sdist bdist_wheel
	twine upload dist/*
	rm -rf dist build .egg sec_edgar_downloader.egg-info
