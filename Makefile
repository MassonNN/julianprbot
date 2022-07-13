generate:
	alembic revision --m="$(NAME)" --autogenerate

migrate:
	alembic upgrade head
