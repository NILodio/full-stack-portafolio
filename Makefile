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

.PHONY: bash
bash:
	docker compose exec backend bash

# alembic revision --autogenerate -m "Add column last_name to User model"
# alembic upgrade head

.PHONY: migrate
migrate:
	docker-compose exec backend bash -c "alembic revision --autogenerate -m '$(argument)' && alembic upgrade head"
