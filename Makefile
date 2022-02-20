isort = isort -w 120
black = black -S -l 120 --target-version py38

.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: format
format:
	isort src/
	$(black) src/

.PHONY: lint
lint:
	flake8 src/
	isort --check-only src/
	$(black) --check src/
