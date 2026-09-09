from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# DEMO SITE - not a deployment template. The values below are deliberately
# permissive so `manage.py runserver` works with no setup; every one of them is
# unsafe in production. See docs/deployment.md for the real checklist.
SECRET_KEY = "example-only-not-secret"
DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_cotton",
    "django_control_components",
    "demo",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "demo" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "builtins": ["django_cotton.templatetags.cotton"],
        },
    }
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# django-control-components - fully self-hosted, no CDN.
DCC = {
    "TABLE_CLIENT_SIDE_MAX_ROWS": 200,
    "VENDOR_ASSETS": True,  # serve htmx / Alpine / focus from web/demo/static/dcc/vendor/
    "VENDOR_ASSET_DIR": "dcc/vendor/",
    "ICON_ASSET_URL": STATIC_URL + "fa/css/all.min.css",  # bundled Font Awesome
    "CHARTJS_URL": STATIC_URL + "dcc/vendor/chart.umd.min.js",
}

# Content-Security-Policy: Alpine needs 'unsafe-eval'. Everything else is 'self'
# (no CDN). (Django 6 native CSP; harmless dict on 5.2 where it is unused.)
SECURE_CSP = {
    "DIRECTIVES": {
        "default-src": ["'self'"],
        "script-src": ["'self'", "'unsafe-eval'"],
        "style-src": ["'self'", "'unsafe-inline'"],
        "img-src": ["'self'", "data:"],
        "font-src": ["'self'"],
    }
}
