"""Browser tests. Opt in with ``-m e2e``; deselected from the default run.

Run: ``uv run nox -s e2e`` or
``uv run pytest --ds=tests.e2e.settings -m e2e tests/e2e``. Needs a Chromium build
(``playwright install chromium``); no network - htmx / Alpine are the bundled
copies under ``web/demo/static/dcc/vendor/``.
"""

from __future__ import annotations

import os

import pytest

# Must be set before pytest-django configures. This conftest is loaded during the
# initial-conftest phase whenever ``tests/e2e`` is on the command line, which is
# early enough; the full-suite run deselects e2e by marker and never needs it.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.e2e.settings")
# Playwright's sync API keeps an event loop on the main thread; pytest-django's
# live_server does its (genuinely synchronous) DB setup on that thread.
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "1")

pytestmark = pytest.mark.e2e


def pytest_configure(config):
    markexpr = str(config.getoption("markexpr", "") or "")
    if "e2e" not in markexpr or "not e2e" in markexpr:
        return  # e2e not selected (the default run deselects it)

    from django.conf import settings

    if settings.SETTINGS_MODULE != "tests.e2e.settings":
        raise pytest.UsageError(
            "the e2e suite needs the demo-backed settings. Run:\n"
            "  uv run nox -s e2e\n"
            "or:\n"
            "  uv run pytest --ds=tests.e2e.settings -m e2e tests/e2e"
        )


@pytest.fixture(autouse=True)
def _mark_e2e(request):
    request.node.add_marker(pytest.mark.e2e)


@pytest.fixture
def browser_context_args(browser_context_args):
    return {**browser_context_args, "viewport": {"width": 1280, "height": 900}}


@pytest.fixture
def page_ready(page):
    """A ``page`` whose ``goto`` also waits for Alpine to have initialised."""

    def _goto(url: str):
        page.goto(url)
        page.wait_for_function("window.Alpine && window.Alpine.version")
        return page

    page.goto_ready = _goto  # type: ignore[attr-defined]
    return page


@pytest.fixture
def no_console_errors(page):
    """Collect severe console messages / page errors for an assertion."""
    errors: list[str] = []
    page.on("console", lambda m: m.type == "error" and errors.append(m.text))
    page.on("pageerror", lambda e: errors.append(str(e)))
    return errors


@pytest.fixture
def studio_user(django_user_model):
    from django.contrib.auth.models import Permission

    user = django_user_model.objects.create_user("editor", password="pw")
    user.user_permissions.add(Permission.objects.get(codename="use_studio"))
    user.is_staff = True
    user.save()
    return django_user_model.objects.get(pk=user.pk)


@pytest.fixture
def login(page, live_server, studio_user):
    """Log ``studio_user`` in through the admin login form and return the page."""

    def _login():
        page.goto(f"{live_server.url}/admin/login/")
        page.fill("#id_username", "editor")
        page.fill("#id_password", "pw")
        page.click("input[type=submit]")
        page.wait_for_load_state("networkidle")
        return page

    return _login
