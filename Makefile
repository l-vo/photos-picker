.DEFAULT_GOAL := help
SHELL := /bin/bash

.PHONY: build help upload upload-test test-distribute valid

## ------

## Build files to distribute on PYPI
build:
	rm dist/*
	python setup.py sdist

## Upload to PYPI
upload:
	python -m twine upload dist/*

## Upload to PYPI test
upload-test:
	python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

## Build and upload on PYPI test
test-distribute: build upload-test

## Launch tox for PEP8 and tests validation
validate:
	tox -c tox.ini

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


