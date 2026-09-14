"""`dccBulk` selection state on a client table with bulk actions: per-row
checkboxes, select-all, the count label, and clear."""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.e2e


def _ready(page):
    page.wait_for_selector("[x-data^='dccTable']")
    page.wait_for_function("window.Alpine && window.Alpine.version")


def test_row_selection_shows_toolbar_and_count(live_server, page):
    page.goto(f"{live_server.url}/e2e/table/")
    _ready(page)
    toolbar = page.locator(".dcc-table__bulk")
    assert not toolbar.is_visible()

    page.locator("td.dcc-table__select input[data-dcc-bulk]").first.check()
    toolbar.wait_for(state="visible")
    assert "1 selected" in toolbar.locator(".dcc-table__bulkcount").text_content()

    page.locator("td.dcc-table__select input[data-dcc-bulk]").nth(1).check()
    assert "2 selected" in toolbar.locator(".dcc-table__bulkcount").text_content()


def test_select_all_header_checkbox(live_server, page):
    page.goto(f"{live_server.url}/e2e/table/")
    _ready(page)
    total = page.locator("td.dcc-table__select input[data-dcc-bulk]").count()
    page.locator("thead input.dcc-check__box").check()
    page.wait_for_function(
        f"() => [...document.querySelectorAll('td.dcc-table__select input')]"
        f".filter(c => c.checked).length === {total}"
    )
    assert page.locator(".dcc-table__bulk").is_visible()


def test_clear_selection(live_server, page):
    page.goto(f"{live_server.url}/e2e/table/")
    _ready(page)
    page.locator("td.dcc-table__select input[data-dcc-bulk]").first.check()
    page.locator(".dcc-table__bulk").wait_for(state="visible")
    page.click(".dcc-table__bulk button:has-text('Clear')")
    page.locator(".dcc-table__bulk").wait_for(state="hidden")
    assert page.locator("td.dcc-table__select input[data-dcc-bulk]:checked").count() == 0
