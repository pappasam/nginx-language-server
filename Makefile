.PHONY: help
help:  ## Print this help menu
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: setup
setup:  ## Set up the local development environment
	poetry install
	poetry run pre-commit install

.PHONY: test
test:  ## Run the tests
	poetry run black --check --diff nginx_language_server
	poetry run docformatter --check --recursive nginx_language_server
	poetry run isort --check nginx_language_server
	poetry run pylint nginx_language_server
	poetry run pyright nginx_language_server

.PHONY: publish
publish:  ## Build & publish the new version
	poetry build
	poetry publish

.PHONY: format
format:
	poetry run black nginx_language_server
	poetry run isort nginx_language_server
	poetry run docformatter --recursive --in-place nginx_language_server
