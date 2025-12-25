#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Install dependencies
pip install -r requirements.txt

# 2. Run migrations
python manage.py migrate --no-input

# 3. CRITICAL: Create the directory and collect files
# The -p flag ensures it doesn't error if the folder exists
mkdir -p staticfiles
python manage.py collectstatic --no-input --clear