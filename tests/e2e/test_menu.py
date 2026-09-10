"""`ui.Menu`: Alpine disclosure - toggle, click-outside close, escape close."""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.e2e


def _ready(page):
    page.wait_for_function("window.Alpine && window.Alpine.version")


def test_menu_toggles_open_and_closed(live_server, page):
    page.goto(f"{live_server.url}/e2e/menu/")
    _ready(page)
    trigger = page.locator(".dcc-menu__trigger")
    menu_list = page.locator(".dcc-menu__list")

    assert not menu_list.is_visible()
    trigger.click()
    menu_list.wait_for(state="visible")
    assert trigger.get_attribute("aria-expanded") == "true"
    assert page.locator("#menu-edit").count() == 1
    assert "Edit" in menu_list.text_content()

    trigger.click()
    menu_list.wait_for(state="hidden")


def test_menu_closes_on_click_outside(live_server, page):
    page.goto(f"{live_server.url}/e2e/menu/")
    _ready(page)
    page.click(".dcc-menu__trigger")
    page.locator(".dcc-menu__list").wait_for(state="visible")
    page.mouse.click(5, 5)
    page.locator(".dcc-menu__list").wait_for(state="hidden")


def test_menu_closes_on_escape(live_server, page):
    page.goto(f"{live_server.url}/e2e/menu/")
    _ready(page)
    page.click(".dcc-menu__trigger")
    page.locator(".dcc-menu__list").wait_for(state="visible")
    page.keyboard.press("Escape")
    page.locator(".dcc-menu__list").wait_for(state="hidden")
