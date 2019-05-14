.PHONY: auto test lint clean cleanbuild publish

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

lint:
	env/bin/flake8 --config=setup.cfg sec_edgar_downloader tests setup.py

clean:
	rm -rf env .pytest_cache ./**/__pycache__
	rm -rf dist build .egg sec_edgar_downloader.egg-info
	rm -f ./**/*.pyc .coverage

publish: clean
	pip install -U twine wheel
	python3 setup.py sdist bdist_wheel
	twine upload dist/*
	rm -rf dist build .egg sec_edgar_downloader.egg-info
