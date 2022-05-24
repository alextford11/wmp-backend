isort = isort -w 120
black = black -S -l 120 --target-version py38

.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: format
format:
	isort src/ tests/
	$(black) src/ tests/

.PHONY: lint
lint:
	flake8 src/ tests/
	isort --check-only src/ tests/
	$(black) --check src/ tests/

.PHONY: reset-db
reset-db:
	psql -h localhost -U postgres -c "DROP DATABASE IF EXISTS wmp_backend"
	psql -h localhost -U postgres -c "CREATE DATABASE wmp_backend"
	psql -h localhost -U postgres -c "DROP DATABASE IF EXISTS wmp_backend_test"
	psql -h localhost -U postgres -c "CREATE DATABASE wmp_backend_test"

.PHONY: rebuild-db
rebuild-db:
	make reset-db
	python manage.py build-workouts

.PHONY: test
test:
	pytest
