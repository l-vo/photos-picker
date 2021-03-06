.DEFAULT_GOAL := help
SHELL := /bin/bash

.PHONY: build clear-tmp help lint upload upload-test test test-distribute valid

## ------

## Build files to distribute on PYPI
build:
	-rm dist/*
	python setup.py sdist bdist_wheel

## Clear remaining temporary files used for functional tests
clear-tmp:
	@if [ -z ${TMPDIR} ]; \
	then \
		if [ -d /tmp/photos-picker-test ]; \
		then \
			rm -rf /tmp/photos-picker-test; \
			echo "/tmp/photos-picker-test removed"; \
		else \
			echo "/tmp/photos-picker-test already removed"; \
		fi \
	else \
		if [ -d ${TMPDIR}/photos-picker-test ]; \
		then \
			rm -rf ${TMPDIR}/photos-picker-test; \
			echo "${TMPDIR}/photos-picker-test removed"; \
		else \
			echo "${TMPDIR}/photos-picker-test already removed"; \
		fi \
	fi

## Install dev requirements
dev:
	pip install -r requirements.txt

## Lint code
lint:
	flake8 photospicker
	flake8 tests

## Upload to PYPI
upload:
	python -m twine upload dist/*

## Upload to PYPI test
upload-test:
	python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

## Run all tests
test: test-unit test-functional

## Run unit tests
test-unit:
	coverage run --source photospicker -m unittest discover tests/unit/
	coverage html
	coverage report

## Run functional tests
test-functional:
	python -m unittest discover tests/functional/

## Build and upload on PYPI test
test-distribute: build upload-test

## Launch PEP8 and tests validation
validate: lint test

## ------

# APPLICATION
APPLICATION := "Photos picker"

# COLORS
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)

TARGET_MAX_CHAR_NUM=20
## Show this help
help:
	@echo '# ${YELLOW}${APPLICATION}${RESET} / ${GREEN}${ENV}${RESET}'
	@echo ''
	@echo 'Usage:'
	@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
	@echo ''
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")); \
			gsub(":", " ", helpCommand); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)s${RESET} ${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST) | sort


