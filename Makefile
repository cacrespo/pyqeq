# Turing's Bluff - PyCamp 2026 Makefile

.PHONY: help install migrate run shell clean-db

help:
	@echo "Comandos disponibles:"
	@echo "  make install    - Instala dependencias con uv"
	@echo "  make migrate    - Genera y aplica migraciones"
	@echo "  make run        - Corre el servidor en 0.0.0.0:8000 (red local)"
	@echo "  make shell      - Abre el shell de Django"
	@echo "  make clean-db   - Borra la base de datos y reinicia las migraciones"

install:
	uv sync

migrate:
	uv run python manage.py makemigrations game
	uv run python manage.py migrate

run:
	@echo "🚀 Iniciando servidor en red local..."
	@echo "Asegurate de compartir tu IP local con los demás jugadores."
	uv run python manage.py runserver 0.0.0.0:8000

shell:
	uv run python manage.py shell_plus --ipython || uv run python manage.py shell

clean-db:
	rm -f db.sqlite3
	find . -path "*/migrations/*.py" ! -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc" -delete
	make migrate
