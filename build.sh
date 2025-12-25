#!/usr/bin/env bash
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run migrations to ensure DB schema is up to date
python manage.py migrate --no-input

# Collect static files
python manage.py collectstatic --no-input