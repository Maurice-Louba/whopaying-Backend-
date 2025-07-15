#!/usr/bin/env bash

set -o errexit

echo "Installing dependencies..."
poetry install --no-root

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Applying migrations..."
python manage.py migrate

