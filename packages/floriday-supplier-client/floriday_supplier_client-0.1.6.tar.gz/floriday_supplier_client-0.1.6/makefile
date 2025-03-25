.phony : tests, bootstrap, update, console, build, documentation, printversion, release, local_specs, client

VERSION := $(shell git describe --tags)
ifeq ($(VERSION),)
    VERSION := v0.0.1
endif

bootstrap:
	python -m venv venv
	@echo "Run 'source venv/bin/activate' to activate the virtual environment, followed by 'make update' to install dependencies."
update:
	python -m pip install --upgrade pip build
	python -m pip install -r requirements.txt
	python -m pip install -r test-requirements.txt
	pip install -e .
console:
tests:
	pytest -m "not integration"
test-integration:
	pytest
	# Run example.py to test integration with Floriday API
	python example.py
build:
	python -m build
quality: tests
	# only run tests for now
documentation:
printversion:
	@python -m setuptools_scm
release:
	@if [ -n "$$(git status --porcelain)" ]; then \
		echo "There are uncommitted changes or untracked files"; \
		exit 1; \
	fi
	@if [ "$$(git rev-parse --abbrev-ref HEAD)" != "main" ]; then \
		echo "Not on main branch"; \
		exit 1; \
	fi
	@if [ "$$(git rev-parse HEAD)" != "$$(git rev-parse origin/main)" ]; then \
		echo "Local branch is ahead of origin"; \
		exit 1; \
	fi
	@git tag v$$(python -m setuptools_scm --strip-dev)
	@git push origin --tags

api_version := 2024v1
url := https://api.staging.floriday.io/suppliers-api-$(api_version)/swagger/UUID/swagger.json
target_dir := .
spec_file := ./specs/floriday-suppliers-api-$(api_version)-swagger-UUID.json

local_specs:
	mkdir -p ./specs
	curl $(url) > $(spec_file)

floriday_supplier_client/api_client.py: $(spec_file)
	swagger-codegen generate -i $(spec_file) -l python -o $(target_dir) -DpackageName=floriday_supplier_client
	rm -f git_push.sh .travis.yml -f tox.ini

client: floriday_supplier_client/api_client.py
