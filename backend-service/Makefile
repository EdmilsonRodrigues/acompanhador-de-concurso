THRESHOLD_COVERAGE ?= 0.8
TAG ?= 1.0.0

.PHONY: install
install:
	poetry install --all-groups

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
	poetry run mypy backend_service

.PHONY: unit
unit:
	poetry run pytest tests/unit

.PHONY: test
test:
	poetry run pytest

.PHONY: ci-test
ci-test:
	poetry run pytest  --cov-report=xml

.PHONY: check-coverage
check-coverage:
	grep "<coverage " coverage.xml | cut -d ' ' -f 6 | cut -d '=' -f 2 | tr -d '"' | awk '{ if ($$1 >= ${THRESHOLD_COVERAGE}) exit 0; else exit 1; }'

.PHONY: build
build:
	docker build -t edmilsonrodrigues/concurso-scraper-service:${TAG} .

.PHONY: docker-test
docker-test:
	docker compose up --exit-code-from scraper


.PHONY: run
run:
	fastapi run backend_service/main.py
