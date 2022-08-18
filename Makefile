isort = isort -w 120
black = black -S -l 120 --target-version py38

.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: format
format:
	isort src/ tests/ alembic/
	$(black) src/ tests/ alembic/

.PHONY: lint
lint:
	flake8 src/ tests/ alembic/
	isort --check-only src/ tests/ alembic/
	$(black) --check src/ tests/ alembic/

.PHONY: reset-db
reset-db:
	psql -h localhost -U postgres -c "DROP DATABASE IF EXISTS wmp_backend"
	psql -h localhost -U postgres -c "CREATE DATABASE wmp_backend"
	psql -h localhost -U postgres -c "DROP DATABASE IF EXISTS wmp_backend_test"
	psql -h localhost -U postgres -c "CREATE DATABASE wmp_backend_test"

.PHONY: build-db
build-db:
	python manage.py build-workouts

.PHONY: rebuild-db
rebuild-db:
	make reset-db
	make build-db

.PHONY: test
test:
	pytest

.PHONY: makemigrations
makemigrations:
	alembic revision --autogenerate -m "$(m)"

.PHONY: migrate
migrate:
	alembic upgrade head
