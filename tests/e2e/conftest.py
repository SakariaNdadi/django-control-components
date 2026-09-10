"""Browser tests. Opt in with ``-m e2e``; deselected from the default run.

Needs a Chromium build (``playwright install chromium``). No network: htmx and
Alpine are served from ``tests/testapp/static/dcc/vendor/`` via
``DCC["VENDOR_ASSETS"]``.
"""

from __future__ import annotations

import os

import pytest

# Playwright's sync API keeps an event loop on the main thread; pytest-django's
# live_server does its DB setup on that thread. The DB work is genuinely sync and
# safe here - this only silences Django's async-context guard for the e2e run.
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "1")

pytestmark = pytest.mark.e2e


@pytest.fixture(autouse=True)
def _mark_e2e(request):
    request.node.add_marker(pytest.mark.e2e)


@pytest.fixture(autouse=True)
def _vendor_assets(settings):
    """Serve htmx/Alpine from the bundled copies so the suite needs no network."""
    settings.DCC = {**getattr(settings, "DCC", {}), "VENDOR_ASSETS": True}


@pytest.fixture
def browser_context_args(browser_context_args):
    return {**browser_context_args, "viewport": {"width": 1280, "height": 900}}
