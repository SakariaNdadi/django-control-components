"""Toast host: `dcc:toast` (string + object) and `dcc:notify` (single + batch)."""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.e2e


def _ready(page):
    page.wait_for_function("window.Alpine && window.Alpine.version")


def test_string_toast(live_server, page):
    page.goto(f"{live_server.url}/e2e/toasts/")
    _ready(page)
    page.click("#toast-string")
    toast = page.locator("#dcc-toasts .dcc-toast").first
    toast.wait_for()
    assert "Saved" in toast.text_content()


def test_object_toast_carries_level_class(live_server, page):
    page.goto(f"{live_server.url}/e2e/toasts/")
    _ready(page)
    page.click("#toast-object")
    toast = page.locator("#dcc-toasts .dcc-toast").first
    toast.wait_for()
    assert "Object toast" in toast.text_content()
    assert "dcc-toast--success" in (toast.get_attribute("class") or "")


def test_notify_is_alert_role(live_server, page):
    page.goto(f"{live_server.url}/e2e/toasts/")
    _ready(page)
    page.click("#toast-notify")
    toast = page.locator("#dcc-toasts .dcc-toast").first
    toast.wait_for()
    assert toast.get_attribute("role") == "alert"
    assert "Notified - now" in toast.text_content()


def test_batch_notify_stacks(live_server, page):
    page.goto(f"{live_server.url}/e2e/toasts/")
    _ready(page)
    page.click("#toast-batch")
    page.wait_for_function("() => document.querySelectorAll('#dcc-toasts .dcc-toast').length >= 2")
    texts = page.eval_on_selector_all(
        "#dcc-toasts .dcc-toast", "els => els.map(e => e.textContent)"
    )
    assert any("One" in t for t in texts) and any("Two" in t for t in texts)
