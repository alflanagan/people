FROM python:3.13.2-slim-bookworm

SHELL ["/bin/bash", "-euo", "pipefail", "-c"]

# I have seen problems with pinning apt packages (versions "disappearing")
# hadolint ignore=DL3008
RUN apt-get update --yes --quiet \
    && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    curl \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Port used by this container to serve HTTP.
EXPOSE 8080

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ENV PYTHONUNBUFFERED=1 \
  PORT=8080

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Install the project requirements.
COPY app/Makefile app/requirements.txt /app/

RUN make setup

# Copy the source code of the project into the container.
COPY app /app/

WORKDIR /app/people
