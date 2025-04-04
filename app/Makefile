# Commands which execute in the docker container for the People app API.

setup:
	python -m pip install uv
	uv sync

django:
	cd people && uv run manage.py shell

server:
	cd people && uv run manage.py runserver 0.0.0.0:8080
