THRESHOLD_COVERAGE ?= 0.8

.PHONY: lint
lint:
	ruff check

.PHONY: format
format:
	ruff format
	ruff check --fix
	ruff format

.PHONY: static
static:
	mypy src

.PHONY: unit
unit:
	pytest -m "not e2e"

.PHONY: e2e
e2e:
	docker compose up db -d
	DATABASE_URL="postgresql://postgres:postgres@localhost:5432/scraper" pytest -m e2e
	docker compose down

.PHONY: test
test:
	docker compose up db -d
	DATABASE_URL="postgresql://postgres:postgres@localhost:5432/scraper" pytest
	docker compose down

.PHONY: ci-test
ci-test:
	docker compose up db -d
	DATABASE_URL="postgresql://postgres:postgres@localhost:5432/scraper" pytest  --cov-report=xml
	docker compose down


.PHONY: check-coverage
check-coverage:
	grep "<coverage " coverage.xml | cut -d ' ' -f 6 | cut -d '=' -f 2 | tr -d '"' | awk '{ if ($$1 >= ${THRESHOLD_COVERAGE}) exit 0; else exit 1; }'

