.PHONY: format
format:
	python -m isort .
	python -m black .
	python -m ruff check . --fix


.PHONY: up-d
up-d:
	docker compose up -d

.PHONY: up
up:
	docker compose up

.PHONY: backend_bash
backend_bash:
	docker compose exec backend bash

.PHONY: reload
reload:
	docker compose exec backend bash /start-reload.sh

.PHONY: test
test:
	docker compose exec backend bash /app/tests-start.sh -x

.PHONY: down
down:
	docker compose down