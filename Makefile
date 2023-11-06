.EXPORT_ALL_VARIABLES:
.PHONY: ci-checks
SHELL := /bin/bash
MAKE_TASKS := \
	mypy ruff flake8 \
	prettier \
	ci-checks

$(MAKE_TASKS):
	./ci-checks/$@.sh

build:
	./m/scripts/build.sh
