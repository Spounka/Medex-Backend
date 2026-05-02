import os

import dj_database_url
from decouple import config

from .base import *

SITE_ORIGIN = config("SITE_ORIGIN", cast=str, default="")
FRONT_SITE_ORIGIN = config("FRONT_SITE_ORIGIN", cast=str, default="")

if not SITE_ORIGIN or not FRONT_SITE_ORIGIN:
    raise RuntimeError("SITE_ORIGIN and FRONT_SITE_ORIGIN not found")

ALLOWED_HOSTS = [SITE_ORIGIN, FRONT_SITE_ORIGIN, "localhost"]
CSRF_TRUSTED_ORIGINS = [
    f"https://{SITE_ORIGIN}",
    f"https://{FRONT_SITE_ORIGIN}",
    "http://localhost",
]

DATABASES = {
    "default": dj_database_url.config(default="sqlite:///" + os.path.join("db.sqlite3"))
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True


CORS_ALLOWED_ORIGINS = [
    "http://localhost",
    "http://127.0.0.1",
    f"https://{SITE_ORIGIN}",
    f"https://{FRONT_SITE_ORIGIN}",
]


MEDIA_ROOT = BASE_DIR / "media"

MEDIA_URL = "/uploads/"

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = "staticfiles"
