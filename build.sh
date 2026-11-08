#!/usr/bin/env bash
# Build script for Render.com deployment
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

mkdir -p logs static_root media

python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py seed_properties
