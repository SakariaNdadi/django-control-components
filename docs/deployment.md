# Deployment

Everything you need to run a DCC project with `DEBUG = False`. The library ships
no models and no migrations of its own (only the dev-only studio does), so there
is nothing to migrate - the work is static files, CSRF, and a short settings
audit.

## Static files

`{% dcc_assets %}` emits `<link>` / `<script>` tags built with Django's
`{% static %}` - the CSS and JS live inside the installed package at
`django_control_components/static/dcc/` (`dcc.css`, `dcc.js`, and, if the studio
extra is installed, `dcc-studio.css` / `dcc-studio.js`).

So a production project needs the normal Django static pipeline:

```python
INSTALLED_APPS = [
    # ...
    "django.contrib.staticfiles",
    "django_cotton",
    "django_control_components",
]

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"   # collectstatic target
```

```bash
python manage.py collectstatic --no-input
```

`collectstatic` copies `dcc/dcc.css` and `dcc/dcc.js` into `STATIC_ROOT`; your
web server (or WhiteNoise) serves them from there.

### WhiteNoise (self-contained deploys)

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",   # right after SecurityMiddleware
    # ...
]
STORAGES = {
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}
```

The manifest storage fingerprints filenames; `{% dcc_assets %}` goes through
`{% static %}`, so the hashed names resolve with no extra work.

## No CDN / air-gapped

By default htmx, Alpine, the Alpine focus plugin and (for `ChartWidget`)
Chart.js load from `https://cdn.jsdelivr.net`, and the icon font from the same.
To serve them from your own static files instead:

```python
DCC = {
    "VENDOR_ASSETS": True,             # emit local <script>/<link> for htmx + Alpine + focus
    "VENDOR_ASSET_DIR": "dcc/vendor/", # static path prefix for the copies
}
```

```bash
python manage.py dcc_vendor_assets --dest path/to/your/static/dcc/vendor/
python manage.py collectstatic --no-input
```

`dcc_vendor_assets` downloads the exact pinned versions the package was built
against. Chart.js and the icon-set CSS are governed separately by
`DCC["ICON_SET"]` / `DCC["ICON_ASSET_URL"]` - point those at local files or a
self-hosting icon set to remove the last CDN references.

If a CDN asset must stay remote, pin its integrity hash:

```python
DCC = {
    "ASSET_SRI": {
        "https://cdn.jsdelivr.net/npm/htmx.org@2.0.4/dist/htmx.min.js": "sha384-...",
    },
}
```

## Content-Security-Policy

Alpine evaluates its directive expressions, so it needs `script-src
'unsafe-eval'`. With the default CDN assets you also need to allow jsDelivr.
Django 6 reads `SECURE_CSP` natively; on 5.2 the dict is harmless and you wire
CSP through your own middleware. Reference policy (from the `web/` project):

```python
_CDN = "https://cdn.jsdelivr.net"
SECURE_CSP = {
    "DIRECTIVES": {
        "default-src": ["'self'"],
        "script-src": ["'self'", "'unsafe-eval'", "'unsafe-inline'", _CDN],
        "style-src": ["'self'", "'unsafe-inline'", _CDN],
        "img-src": ["'self'", "data:"],
    }
}
```

`VENDOR_ASSETS = True` plus a self-hosting icon set lets you drop `_CDN` from
`script-src` / `style-src`. `'unsafe-eval'` stays - it is Alpine's requirement,
not the package's.

## CSRF

DCC's table mutations, action confirms and live field validation are POSTs made
by htmx / `dcc.js`. They rely on the `csrftoken` cookie being present on the
page. See [settings.md](settings.md#csrf) - put `{% csrf_token %}` in your base
layout or decorate the host view with `@ensure_csrf_cookie`. This is the most
common "works in dev, 403s in prod" cause.

## `DEBUG = False` checklist

- [ ] `collectstatic` run; `STATIC_ROOT` served.
- [ ] `ALLOWED_HOSTS` set.
- [ ] CSRF cookie guaranteed on every page that renders a table / action /
      `.live()` field (see above).
- [ ] **Remove `django_control_components.studio` from `INSTALLED_APPS`.** It is
      a dev-only prototyping tool; leaving it in with `DEBUG = False` raises
      system check `dcc_studio.W003`. Its URL include and `{% dcc_studio_assets %}`
      go too.
- [ ] `python manage.py check --deploy` is clean.
- [ ] Any `Panel` has `.auth(...)` guards; resources implement `can()` if model
      perms are not enough.
- [ ] CSP allows what your chosen asset strategy needs.

## Where to go next

- [settings.md](settings.md) - every `DCC[...]` key, the minimal base template,
  CSRF, system checks.
- [testing.md](testing.md) - testing views and components.
