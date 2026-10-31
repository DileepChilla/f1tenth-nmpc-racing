.PHONY: build shell test lint

build:
	docker compose -f docker/docker-compose.yml build

shell:
	docker compose -f docker/docker-compose.yml run --rm nmpc

# Run inside the container:
test:
	pip3 install -e ".[dev]" && pytest

lint:
	ruff check src tests
