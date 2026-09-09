from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

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
    # Not used for a studio-authored resource here (the catalog is dev-only per
    # its own docs) - installed only because panels/nav.py's stored-nav lookup
    # imports django_control_components.studio.models unconditionally whenever
    # the package is importable, regardless of INSTALLED_APPS, and needs its
    # migrations applied to avoid an OperationalError.
    "django_control_components.studio",
    "demo",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
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
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# django-control-components
DCC = {
    "TABLE_CLIENT_SIDE_MAX_ROWS": 200,
    # No admin/studio UI mounted in this project - the catalog is its own panel.
    "STUDIO_ADMIN_ENTRY": False,
}

# Content-Security-Policy: Alpine needs 'unsafe-eval'. htmx, Alpine, Chart.js and
# the icon font all load from the jsdelivr CDN. Everything else stays tight.
# (Django 6 native CSP; harmless dict on 5.2 where it is simply unused.)
_CDN = "https://cdn.jsdelivr.net"
SECURE_CSP = {
    "DIRECTIVES": {
        "default-src": ["'self'"],
        "script-src": ["'self'", "'unsafe-eval'", "'unsafe-inline'", _CDN],
        "style-src": ["'self'", "'unsafe-inline'", _CDN],
        "img-src": ["'self'", "data:"],
    }
}
