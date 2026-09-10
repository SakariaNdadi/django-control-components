"""Chrome blocks with live endpoints: `dccGlobalSearch` (debounced fetch,
results panel, click-outside) and `dccBell` (poll, badge, dropdown, mark-read)."""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.e2e


def _ready(page):
    page.wait_for_function("window.Alpine && window.Alpine.version")


def test_global_search_fetches_and_shows_results(live_server, page):
    page.goto(f"{live_server.url}/e2e/blocks/")
    _ready(page)
    results = page.locator(".dcc-globalsearch__results")

    page.fill(".dcc-globalsearch__input", "widgets")
    results.wait_for(state="visible")
    assert "Result for widgets" in results.text_content()

    page.mouse.click(2, 2)
    results.wait_for(state="hidden")


def test_global_search_empty_query_hides_panel(live_server, page):
    page.goto(f"{live_server.url}/e2e/blocks/")
    _ready(page)
    page.fill(".dcc-globalsearch__input", "abc")
    page.locator(".dcc-globalsearch__results").wait_for(state="visible")
    page.fill(".dcc-globalsearch__input", "")
    page.locator(".dcc-globalsearch__results").wait_for(state="hidden")


def test_bell_polls_badge_and_opens_list(live_server, page):
    page.goto(f"{live_server.url}/e2e/blocks/")
    _ready(page)
    badge = page.locator(".dcc-bell__badge")
    badge.wait_for(state="visible")
    assert badge.text_content().strip() == "2"

    page.click(".dcc-bell__button")
    page.locator(".dcc-bell__menu").wait_for(state="visible")
    assert page.locator(".dcc-bell__item").count() == 2
    assert "Build passed" in page.locator(".dcc-bell__list").text_content()


def test_bell_mark_all_read_clears_badge(live_server, page):
    page.goto(f"{live_server.url}/e2e/blocks/")
    _ready(page)
    page.locator(".dcc-bell__badge").wait_for(state="visible")
    page.click(".dcc-bell__button")
    page.click(".dcc-bell__mark")
    page.locator(".dcc-bell__badge").wait_for(state="hidden")


def test_bell_refreshes_on_dcc_refresh_event(live_server, page):
    page.goto(f"{live_server.url}/e2e/blocks/")
    _ready(page)
    page.locator(".dcc-bell__badge").wait_for(state="visible")
    # the bell listens for dcc:refresh on its own root
    page.evaluate(
        "document.querySelector('.dcc-bell').dispatchEvent("
        "new CustomEvent('dcc:refresh', {bubbles:true}))"
    )
    page.wait_for_timeout(200)
    assert page.locator(".dcc-bell__badge").text_content().strip() == "2"
