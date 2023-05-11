.DEFAULT_GOAL := run
.PHONY: run clean

setup: requirements.txt
	pip install -r requirements.txt

run: setup
	python3 parse/test.py

clean:
	rm -rf parse/__pycache__
