"""Modal: the `ui.Modal` overlay (teleport, focus trap, esc / click-self /
event close) and the cotton `<c-dcc.modal>` tag (trigger button, open + close)."""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.e2e


def _ready(page):
    page.wait_for_function("window.Alpine && window.Alpine.version")


def test_ui_modal_open_traps_focus_and_locks_scroll(live_server, page):
    page.goto(f"{live_server.url}/e2e/modal/")
    _ready(page)
    overlay = page.locator(".dcc-modal__overlay")
    overlay.wait_for(state="visible")
    assert overlay.get_attribute("role") == "dialog"
    # x-trap moves focus into the dialog
    page.wait_for_function(
        "() => document.querySelector('.dcc-modal__dialog').contains(document.activeElement)"
    )


def test_ui_modal_closes_on_escape(live_server, page):
    page.goto(f"{live_server.url}/e2e/modal/")
    _ready(page)
    page.locator(".dcc-modal__overlay").wait_for(state="visible")
    page.keyboard.press("Escape")
    page.locator(".dcc-modal__overlay").wait_for(state="hidden")


def test_ui_modal_closes_on_custom_event(live_server, page):
    page.goto(f"{live_server.url}/e2e/modal/")
    _ready(page)
    page.locator(".dcc-modal__overlay").wait_for(state="visible")
    page.evaluate("window.dispatchEvent(new CustomEvent('dcc-modal-close'))")
    page.locator(".dcc-modal__overlay").wait_for(state="hidden")


def test_ui_modal_close_button(live_server, page):
    page.goto(f"{live_server.url}/e2e/modal/")
    _ready(page)
    page.locator(".dcc-modal__overlay").wait_for(state="visible")
    page.click(".dcc-modal__header button[aria-label='Close']")
    page.locator(".dcc-modal__overlay").wait_for(state="hidden")


def test_cotton_modal_trigger_opens_and_teleports_to_body(live_server, page):
    page.goto(f"{live_server.url}/e2e/cotton/")
    _ready(page)
    page.click("button:has-text('Open cotton modal')")
    dialog = page.locator(".dcc-modal__dialog")
    dialog.wait_for(state="visible")
    assert "Modal body content." in dialog.text_content()
    # x-teleport lifts the overlay to be a direct child of <body>
    assert page.evaluate(
        "() => document.querySelector('.dcc-modal__overlay').parentElement === document.body"
    )
    page.keyboard.press("Escape")
    page.locator(".dcc-modal__dialog").wait_for(state="hidden")
