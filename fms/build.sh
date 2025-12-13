#!/usr/bin/env bash
# build.sh
# Exit immediately if a command exits with a non-zero status
set -e

# Install dependencies (already handled by Render, but good practice)
# pip install -r requirements.txt

# Run collectstatic to prepare static files for WhiteNoise
python manage.py collectstatic --no-input