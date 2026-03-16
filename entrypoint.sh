#!/bin/sh
set -e


python3 manage.py createsuperuser --noinput --full_name "Super Administrator" --email "${DJANGO_SUPERUSER_EMAIL}" --phone "${DJANGO_SUPERUSER_PHONE}" || true

python3 manage.py runserver 0.0.0.0:8000

exec "$@"
