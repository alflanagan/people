setup:
	python -m venv .venv
	. .venv/bin/activate \
    && pip install --no-cache-dir wheel pip-tools \
    && pip-sync

django:
	cd people && /app/.venv/bin/python manage.py shell

