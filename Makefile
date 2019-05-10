.PHONY: auto clean cleanall

auto: build37

build36:
	virtualenv env --python=python3.6
	env/bin/pip install -r requirements.txt

build37:
	virtualenv env --python=python3.7
	env/bin/pip install -r requirements.txt

test:
	. env/bin/activate && pytest

clean:
	rm -rf env .pytest_cache
	rm -f sec_edgar_downloader/*.pyc tests/*.pyc

cleanbuild: clean
	rm -rf sec_edgar_downloader.egg-info dist build
