.PHONY: build shell test lint

build:
	docker compose -f docker/docker-compose.yml build

shell:
	docker compose -f docker/docker-compose.yml run --rm nmpc

# Run inside the container:
test:
	PYTHONPATH=src python3 -m pytest -q

lint:
	ruff check src tests
