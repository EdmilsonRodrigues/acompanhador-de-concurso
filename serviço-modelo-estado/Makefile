THRESHOLD_COVERAGE ?= 0.8
TAG ?= 1.0.0

.PHONY: install
install:
	poetry install --all-groups
	poetry run spacy download pt_core_news_sm

.PHONY: lint
lint:
	poetry run ruff check

.PHONY: format
format:
	poetry run ruff format
	poetry run ruff check --fix
	poetry run ruff format

.PHONY: static
static:
	echo "Static tests not implemented"

.PHONY: unit
unit:
	echo "Unit tests not implemented"

.PHONY: e2e
e2e:
	echo "E2E tests not implemented"

.PHONY: test
test:
	echo "Test not implemented"

.PHONY: ci-test
ci-test:
	echo "CI tests not implemented"


.PHONY: check-coverage
check-coverage:
	echo "Check coverage not implemented"

.PHONY: build
build:
	echo "Build not implemented"

.PHONY: docker-test
docker-test:
	echo "Docker test not implemented"
