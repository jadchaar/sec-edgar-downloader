.PHONY: auto build36 build37 build38 test flake8 format clean cleanbuild publish

auto: build37

build36:
	virtualenv env --python=python3.6
	env/bin/pip install -r requirements.txt

build37:
	virtualenv env --python=python3.7
	env/bin/pip install -r requirements.txt

build38:
	virtualenv env --python=python3.8
	env/bin/pip install -r requirements.txt

test:
	rm -f .coverage
	. env/bin/activate && pytest --cov-config=setup.cfg --cov=sec_edgar_downloader tests

flake8:
	env/bin/flake8 sec_edgar_downloader tests setup.py

format:
	black sec_edgar_downloader tests setup.py --line-length 120 --target-version py36

clean:
	rm -rf env .pytest_cache ./**/__pycache__
	rm -rf dist build .egg sec_edgar_downloader.egg-info
	rm -f ./**/*.pyc .coverage

publish: clean
	pip install -U twine wheel
	python3 setup.py sdist bdist_wheel
	twine upload dist/*
	rm -rf dist build .egg sec_edgar_downloader.egg-info
