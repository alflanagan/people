setup:
	python -m venv /.venv
	. /.venv/bin/activate \
    && pip install --no-cache-dir wheel pip-tools \
    && pip-sync

django:
	cd people && /.venv/bin/python manage.py shell

server:
	/.venv/bin/python /app/people/manage.py runserver 0.0.0.0:8080
