.PHONY: run test test-cov lint format precommit-install up down shell sec contracts clean-pyc

COMPOSE_DEV = docker compose -f infra/docker-compose.yml

run:
	uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

test:
	PYTHONPATH=. pytest -q

test-cov:
	PYTHONPATH=. pytest --cov=src --cov-report=term-missing

lint:
	ruff check --config=ruff.toml src/ --fix

format:
	ruff check --config=pyproject.toml src --fix --select I --exclude "migrations"
	ruff format src

precommit-install:
	python -m pip install pre-commit && pre-commit install

build:
	$(COMPOSE_DEV) build --no-cache

alembic-rev:
	alembic -c infra/alembic.ini revision --autogenerate -m "$(m)"

alembic-up:
	alembic -c infra/alembic.ini upgrade head

alembic-down:
	alembic -c infra/alembic.ini downgrade -1

up:
	$(COMPOSE_DEV) up

down:
	$(COMPOSE_DEV) down

shell:
	$(COMPOSE_DEV) exec -it app bash

sec:
	bandit -r src && \
	pip-audit -r requirements-tests.txt

contracts:
	lint-imports

clean-pyc:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
