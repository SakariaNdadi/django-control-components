# django-control-components-studio

A **development-only** prototyping tool for
[django-control-components](https://github.com/SakariaNdadi/django-control-components),
in the spirit of `django-debug-toolbar`: wire up panel resources, dashboards,
nav, and role access from the browser to try backend ideas fast, then build
the real UI. `manage.py check` warns if it's installed with `DEBUG=False` —
pull it out of `INSTALLED_APPS` before deploying.

## Install

```bash
pip install "django-control-components[studio]"
```

That pulls this package. Then add the app **after** the core app:

```python
INSTALLED_APPS = [
    # ...
    "django_cotton",
    "django_control_components",
    "django_control_components.studio",
]
```

Run migrations (`dcc_studio` app) and mount a panel with `.studio()` / `.dynamic()`.
See the [no-code docs](https://github.com/SakariaNdadi/django-control-components/blob/master/docs/no-code.md).
