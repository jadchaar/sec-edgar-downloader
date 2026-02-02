.PHONY: auto test docs clean tag

auto: build314

build310: PYTHON_VER = python3.10
build311: PYTHON_VER = python3.11
build312: PYTHON_VER = python3.12
build313: PYTHON_VER = python3.13
<<<<<<< Updated upstream

build310 build311 build312 build313: clean
=======
build314: PYTHON_VER = python3.14

build310 build311 build312 build313 build314: clean
>>>>>>> Stashed changes
	$(PYTHON_VER) -m venv venv
	. venv/bin/activate; \
	pip install -U pip setuptools wheel; \
	pip install -r requirements/requirements-docs.txt; \
	pip install -r requirements/requirements-tests.txt; \
	pre-commit install

test:
	rm -f .coverage coverage.xml
	. venv/bin/activate; \
	pytest

lint:
	. venv/bin/activate; \
	pre-commit run --all-files --show-diff-on-failure

docs: clean-docs
	. venv/bin/activate; \
	cd docs; \
	make html

live-docs: clean-docs
	. venv/bin/activate; \
	sphinx-autobuild docs docs/_build/html

build-dist: clean-dist
	. venv/bin/activate; \
	pip install -U flit; \
	flit build

deep-clean-dry-run:
	git clean -xdn

deep-clean:
	git clean -xdf

clean-env:
	rm -rf venv .tox

clean-dist:
	rm -rf dist build *.egg *.eggs *.egg-info

clean-docs:
	rm -rf docs/_build

clean: clean-env clean-dist clean-docs
	rm -rf .pytest_cache ./**/__pycache__ .mypy_cache
	rm -f .coverage coverage.xml ./**/*.pyc

tag:
	@read -p "Has __version__ been updated for release? (Y/N): " choice; \
	if [ "$$(echo "$$choice" | tr '[:upper:]' '[:lower:]')" = "y" ]; then \
		TAG_VERSION=$$(grep -oE '([0-9]+\.[0-9]+\.[0-9]+)' sec_edgar_downloader/_version.py); \
		echo "Creating and pushing Git tag: $$TAG_VERSION"; \
		git tag $$TAG_VERSION master; \
		git push origin $$TAG_VERSION; \
	else \
		echo "Aborting."; \
	fi
