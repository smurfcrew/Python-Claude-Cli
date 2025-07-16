# MAKEFILE for claude
.PHONY: help install install-dev test from  lin clean run

help:
	@echo "Available commands:"
	@echo "  install 		- Install production dependencies"
	@echo "  install-dev 	- Install development dependencies"
	@echo "  test 			- Run test"
	@echo "  format			- Format code with black and isort"
	@echo "  lint			- Run linting with flake8 and mypy" 
	@echo "  clean 			- Clean up temporary files" 
	@echo "  run			- Run the CLI in interactive mode"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	python -m pytest test_cli.py -v

format:
	black *.py
	isort *.py

lint:
	flake8 *.py
	mypy *.py

clean:
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf *.pyc
	rm -rf *mypy_cache/
	rm -rf *build/
	rm -rf dist/
	rm -rf *.egg-info/

run:
	python cli.py --interactive


example-singles:
	python cli.py --message "Hello, Claude!"

example-file:
	echo "What is Python" > example.txt
	python cli.py --file example.txt
	rm example.txt