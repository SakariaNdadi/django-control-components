"""The standalone studio builder: access control, the hub, the index pages, and
the page builder (`dccTree` + palette + save)."""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.e2e


def _ready(page):
    page.wait_for_function("window.Alpine && window.Alpine.version")


def test_hub_redirects_anonymous(live_server, page):
    resp = page.goto(f"{live_server.url}/studio/")
    assert "/login" in page.url or (resp is not None and resp.status in (302, 403))


def test_hub_renders_for_authorized_user(live_server, page, login):
    login()
    page.goto(f"{live_server.url}/studio/")
    _ready(page)
    body = page.locator("body").text_content()
    assert "Studio" in body
    assert page.locator("a[href*='/studio/pages/']").count() >= 1


@pytest.mark.parametrize("path", ["pages/", "resources/", "dashboards/"])
def test_index_pages_render(live_server, page, login, path):
    login()
    resp = page.goto(f"{live_server.url}/studio/{path}")
    assert resp is not None and resp.status == 200
    _ready(page)


def test_page_builder_shell_boots(live_server, page, login):
    login()
    page.goto(f"{live_server.url}/studio/pages/")
    _ready(page)
    page.fill("input[name='title']", "E2E built page")
    page.click("form button:has-text('Create')")

    page.wait_for_url("**/studio/pages/*/")
    _ready(page)

    # the builder's Alpine root initialised and its three panes rendered
    page.wait_for_selector("[x-data^='dccTree']")
    assert page.locator(".dcc-studio__palette-item").count() > 0
    assert page.locator(".dcc-tree__label").count() >= 1
    assert page.locator(".dcc-studio__btn--primary").is_visible()
    # dccTree parsed its boot JSON without a console error
    assert page.evaluate(
        "() => !!window.Alpine.$data(document.querySelector('[x-data^=\"dccTree\"]'))"
    )


def test_page_builder_undo_redo_present(live_server, page, login):
    login()
    page.goto(f"{live_server.url}/studio/pages/")
    _ready(page)
    page.fill("input[name='title']", "Undo redo page")
    page.click("form button:has-text('Create')")
    page.wait_for_url("**/studio/pages/*/")
    _ready(page)
    assert page.locator("button:has-text('Undo')").is_visible()
    assert page.locator("button:has-text('Redo')").is_visible()
