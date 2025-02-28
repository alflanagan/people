# These are tasks to be run OUTSIDE of the docker environment
# primarily they are concerned with setup, starting, and stopping the environment
PIP_COMPILE = pip-compile --generate-hashes --allow-unsafe --resolver=backtracking

stop:
	docker compose down --remove-orphans

start:
	docker compose up --wait

#start a shell running in the django environment
dev:
	docker exec -it django bash

#TODO: add a task to create the virtual environment

requirements:
	cd app && . .venv/bin/activate && $(PIP_COMPILE) requirements.in

# this makes up for the fact that make has no command to show what tasks are defined
# no attempt was made at a universal solution; you'll need to enhance for any but most basic case
targets:
	@grep -E '^[a-zA-Z_-]+:' Makefile | cut -d: -f1 | grep -v targets
