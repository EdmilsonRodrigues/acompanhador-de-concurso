THRESHOLD_COVERAGE ?= 0.8
TAG ?= 1.0.0

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
	poetry run mypy src

.PHONY: unit
unit:
	poetry run pytest -m "not e2e"

.PHONY: e2e
e2e:
	docker compose up db -d
	DATABASE_URL="postgresql://postgres:postgres@localhost:5432/scraper" poetry run pytest -m e2e
	docker compose down

.PHONY: test
test:
	docker compose up db -d
	DATABASE_URL="postgresql://postgres:postgres@localhost:5432/scraper" poetry run pytest
	docker compose down

.PHONY: ci-test
ci-test:
	docker compose up db -d
	DATABASE_URL="postgresql://postgres:postgres@localhost:5432/scraper" poetry run pytest  --cov-report=xml
	docker compose down


.PHONY: check-coverage
check-coverage:
	grep "<coverage " coverage.xml | cut -d ' ' -f 6 | cut -d '=' -f 2 | tr -d '"' | awk '{ if ($$1 >= ${THRESHOLD_COVERAGE}) exit 0; else exit 1; }'

.PHONY: build
build:
	docker build -t edmilsonrodrigues/concurso-scraper-service:${TAG} .
