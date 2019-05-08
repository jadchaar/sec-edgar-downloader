.PHONY: auto clean

auto: build37

build36:
	virtualenv env --python=python3.6
	env/bin/pip install -r requirements.txt

build37:
	virtualenv env --python=python3.7
	env/bin/pip install -r requirements.txt

clean:
	rm -rf env
	rm -f sec_edgar_downloader/*.pyc tests/*.pyc
