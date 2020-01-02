
.PHONY: build
build:
	@make clean
	@python setup.py sdist bdist_wheel
	@twine check dist/*
	@python setup.py clean --all
	ls -lh dist/*

.PHONY: check
check:
	python setup.py check
	pylama
	mypy readmemaker/ --show-error-context --show-error-codes --ignore-missing-imports --python-version 3.5

.PHONY: clean
clean:
	@rm -rf  \
		dist/ \
		pip-wheel-metadata/ \
		.eggs/ \
		.pytest_cache/ \
		.tox/ \
		**/*/__pycache__/ \
		*.egg-info/
	@find . -not -path '*/\.*' -type f | grep -E .+\.py\.[a-z0-9]{32,}\.py$ | xargs -r rm

.PHONY: fmt
fmt:
	@black $(CURDIR)
	@autoflake --in-place --recursive --remove-all-unused-imports --exclude "__init__.py" .
	@isort --apply --recursive

.PHONY: release
release:
	@python setup.py release --sign
	@make clean
