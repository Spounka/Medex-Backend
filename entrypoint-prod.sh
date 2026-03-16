#!/bin/sh
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Preparing media directories..."
mkdir -p media/product/images/placeholders
mkdir -p media/brand/images/placeholders
mkdir -p media/category/images/placeholders
mkdir -p media/advertisements/files

echo "Extracting placeholder assets..."
if [ -f fixtures/medicinal_asset_pack.zip ]; then
    unzip -o fixtures/medicinal_asset_pack.zip -d fixtures/
    mv fixtures/brand_images/* media/brand/images/placeholders/ 2>/dev/null || true
    mv fixtures/category_images/* media/category/images/placeholders/ 2>/dev/null || true
    mv fixtures/product_images/* media/product/images/placeholders/ 2>/dev/null || true
fi

echo "Loading fixtures..."
python manage.py loaddata fixtures/min_seed.json || true
python manage.py shell < fixtures/seed_medicinal_catalog.py || true
python manage.py shell < fixtures/reassign_catalog_images.py || true

echo "Collecting Static files"
python manage.py collectstatic --noinput

if [ "${DJANGO_CREATE_SUPERUSER}" = "1" ]; then
echo "Creating superuser..."
python manage.py shell <<'PY'
import os
from django.contrib.auth import get_user_model

User = get_user_model()
email = os.getenv("DJANGO_SUPERUSER_EMAIL")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD")
phone = os.getenv("DJANGO_SUPERUSER_PHONE")
full_name = os.getenv("DJANGO_SUPERUSER_FULL_NAME", "Super Administrator")

print(email, password)

if email and password and not User.objects.filter(email=email).exists():
    User.objects.create_superuser(
        email=email,
        password=password,
        full_name=full_name,
        phone=phone,
    )
    print("Superuser created.")
else:
    print("Superuser skipped.")
PY
fi

exec "$@"
