"""`dccShell`: rail collapse + persistence, theme cycle + persistence, and the
mobile nav drawer (scrim, body scroll-lock)."""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.e2e


def _ready(page):
    page.wait_for_function("window.Alpine && window.Alpine.version")


def test_rail_toggle_persists_across_reload(live_server, page):
    page.goto(f"{live_server.url}/e2e/shell/")
    _ready(page)
    panel = page.locator(".dcc-panel")
    assert "is-railed" not in (panel.get_attribute("class") or "")

    page.click(".dcc-panel__railtoggle")
    page.wait_for_function(
        "() => document.querySelector('.dcc-panel').classList.contains('is-railed')"
    )
    assert page.evaluate("localStorage.getItem('dcc-nav-railed')") == "1"

    page.reload()
    _ready(page)
    assert "is-railed" in (page.locator(".dcc-panel").get_attribute("class") or "")
    # no flash: the boot script seeds the class before first paint
    assert page.evaluate("document.documentElement.classList.contains('dcc-pre-railed')")


def test_theme_cycle_sets_data_theme_and_persists(live_server, page):
    page.goto(f"{live_server.url}/e2e/shell/")
    _ready(page)
    page.click(".dcc-nav__theme")
    page.wait_for_function("() => document.documentElement.getAttribute('data-theme') === 'light'")
    page.click(".dcc-nav__theme")
    page.wait_for_function("() => document.documentElement.getAttribute('data-theme') === 'dark'")
    assert page.evaluate("localStorage.getItem('dcc-theme')") == "dark"

    page.reload()
    _ready(page)
    assert page.evaluate("document.documentElement.getAttribute('data-theme')") == "dark"


def test_mobile_nav_drawer_and_scroll_lock(live_server, page):
    page.set_viewport_size({"width": 420, "height": 800})
    page.goto(f"{live_server.url}/e2e/shell/")
    _ready(page)

    page.click(".dcc-panel__navtoggle")
    page.wait_for_function(
        "() => document.querySelector('.dcc-panel').classList.contains('is-nav-open')"
    )
    assert page.evaluate("document.body.classList.contains('dcc-no-scroll')")

    page.click(".dcc-panel__scrim")
    page.wait_for_function(
        "() => !document.querySelector('.dcc-panel').classList.contains('is-nav-open')"
    )
    assert not page.evaluate("document.body.classList.contains('dcc-no-scroll')")
