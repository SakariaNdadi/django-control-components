"""Settings for the Playwright suite (`pytest -m e2e tests/e2e`).

Layers the `web/demo` project on top of `tests.settings`: the demo panel is the
exhaustive fixture (one live render of every catalog component, plus resource /
table / widget pages), and the demo app seeds a handful of `Task` rows on
migrate so those pages have real data. htmx / Alpine are served from the
bundled `web/demo/static/dcc/vendor/` copies - the suite needs no network.
"""

from __future__ import annotations

import sys
from pathlib import Path

from tests.settings import *  # noqa: F403

_REPO_ROOT = Path(__file__).resolve().parents[2]
_WEB = _REPO_ROOT / "web"
if str(_WEB) not in sys.path:
    sys.path.insert(0, str(_WEB))

INSTALLED_APPS = [*INSTALLED_APPS, "demo"]  # noqa: F405

BASE_DIR = _WEB  # demo pages/reference.py reads settings.BASE_DIR

ROOT_URLCONF = "tests.e2e.urls"

TEMPLATES[0]["DIRS"] = [  # noqa: F405
    _WEB / "demo" / "templates",
    Path(__file__).resolve().parent / "templates",
]

STATICFILES_DIRS = [_WEB / "demo" / "static"]

MEDIA_ROOT = "/tmp/dcc-e2e-media"

DCC = {
    "VENDOR_ASSETS": True,
    "VENDOR_ASSET_DIR": "dcc/vendor/",
    "CHARTJS_URL": STATIC_URL + "dcc/vendor/chart.umd.min.js",  # noqa: F405
    "TABLE_CLIENT_SIDE_MAX_ROWS": 200,
    "STUDIO_MODELS": ["demo.Task"],
    "STUDIO_RESOURCE_MODELS": ["demo.Task"],
}
