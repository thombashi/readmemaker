PYTHON := python3

AUTHOR := Tsuyoshi Hombashi
FIRST_RELEASE_YEAR := 2016
LAST_UPDATE_YEAR := $(shell git log -1 --format=%cd --date=format:%Y)


.PHONY: build
build: clean
	@$(PYTHON) -m tox -e build
	ls -lh dist/*

.PHONY: check
check:
	@$(PYTHON) -m tox -e lint

.PHONY: clean
clean:
	@$(PYTHON) -m tox -e clean

.PHONY: fmt
fmt:
	@$(PYTHON) -m tox -e fmt

.PHONY: release
release:
	@$(PYTHON) setup.py release --sign
	@$(MAKE) clean

.PHONY: setup-ci
setup-ci:
	@$(PYTHON) -m pip install --disable-pip-version-check --upgrade releasecmd tox

.PHONY: setup-dev
setup-dev: setup-ci
	@$(PYTHON) -m pip install -q --disable-pip-version-check --upgrade -e .[test]
	@$(PYTHON) -m pip check

.PHONY: update-copyright
update-copyright:
	sed -i "s/^__copyright__ = .*/__copyright__ = f\"Copyright $(FIRST_RELEASE_YEAR)-$(LAST_UPDATE_YEAR), {__author__}\"/" readmemaker/__version__.py
	sed -i "s/^Copyright (c) .* $(AUTHOR)/Copyright (c) $(FIRST_RELEASE_YEAR)-$(LAST_UPDATE_YEAR) $(AUTHOR)/" LICENSE
