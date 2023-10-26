CODE_FOLDERS := src
TEST_FOLDERS := tests

.PHONY: install test format lint security_checks build test_on_docker

install:
	poetry install

test:
	poetry run pytest

format:
	black $(CODE_FOLDERS) $(TEST_FOLDERS)
	isort $(CODE_FOLDERS) $(TEST_FOLDERS)


lint:
	isort --check .
	black --check .
	flake8 $(CODE_FOLDERS) $(TEST_FOLDERS)
	pylint $(CODE_FOLDERS)
	mypy $(CODE_FOLDERS) $(TEST_FOLDERS)

build_test_docker:
	docker build -f docker/tests/Dockerfile -t py3-10-test .

test_on_docker:
	docker run -t py3-10-test make test

lint_on_docker:
	docker run -t py3-10-test make lint

security_check:
	bandit $(CODE_FOLDERS) $(TEST_FOLDERS)

security_check_on_docker:
	docker run -t py3-10-test make security_check