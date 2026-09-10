"""`layout.Tabs` (rendered by a Schema): switching tab shows the matching
panel and moves `aria-selected`."""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.e2e


def _ready(page):
    page.wait_for_function("window.Alpine && window.Alpine.version")


def test_tab_switch_shows_panel(live_server, page):
    page.goto(f"{live_server.url}/e2e/tabs/")
    _ready(page)
    tabs = page.locator(".dcc-tabs__tab")
    panels = page.locator(".dcc-tabs__panel")

    assert tabs.nth(0).get_attribute("aria-selected") == "true"
    assert panels.nth(0).is_visible()
    assert not panels.nth(1).is_visible()

    tabs.nth(1).click()
    page.wait_for_function(
        "() => document.querySelectorAll('.dcc-tabs__panel')[1].offsetParent !== null"
    )
    assert tabs.nth(1).get_attribute("aria-selected") == "true"
    assert tabs.nth(0).get_attribute("aria-selected") == "false"
    assert not panels.nth(0).is_visible()
    assert panels.nth(1).locator(".dcc-field").is_visible()
    assert panels.nth(1).locator("input[name='featured']").count() == 1
