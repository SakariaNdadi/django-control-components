"""`dccForm` reactive visibility: a `visible_when` field appears / disappears
as its controlling field changes, driven by `$dccField`."""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.e2e


def _ready(page):
    page.wait_for_function("window.Alpine && window.Alpine.version")


def test_visible_when_field_reacts_to_controlling_select(live_server, page):
    page.goto(f"{live_server.url}/e2e/form/")
    _ready(page)

    slug = page.locator("input[name='slug']").locator(
        "xpath=ancestor::div[contains(@class,'dcc-field')]"
    )
    # status defaults to "draft" -> slug hidden
    assert not slug.is_visible()

    page.select_option("select[name='status']", "live")
    slug.wait_for(state="visible")

    page.select_option("select[name='status']", "draft")
    slug.wait_for(state="hidden")


def test_form_renders_inside_dccform_wrapper(live_server, page):
    page.goto(f"{live_server.url}/e2e/form/")
    _ready(page)
    assert page.locator(".dcc-form[x-data='dccForm']").count() == 1
    assert page.locator("form input[name='title']").is_visible()
