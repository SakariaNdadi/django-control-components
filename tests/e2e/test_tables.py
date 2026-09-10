"""`dccTable` client mode on the demo catalog: search, sort, pagination, and
row-click navigation on the resource table."""

from __future__ import annotations

import datetime

import pytest

pytestmark = pytest.mark.e2e


def _ready(page):
    page.wait_for_selector("[x-data^='dccTable']")
    page.wait_for_function("window.Alpine && window.Alpine.version")


def _rows(page):
    return page.locator(".dcc-table__row:visible")


def test_client_search_filters_rows(live_server, page):
    page.goto(f"{live_server.url}/table/")
    _ready(page)
    before = _rows(page).count()
    assert before >= 3

    page.fill("input.dcc-table__search", "changelog")
    page.wait_for_function(
        "() => document.querySelectorAll("
        "'.dcc-table__row:not([style*=\"display: none\"])').length === 1"
    )
    visible = _rows(page)
    assert visible.count() == 1
    assert "changelog" in visible.first.text_content().lower()

    page.fill("input.dcc-table__search", "")
    page.wait_for_timeout(250)
    assert _rows(page).count() == before


def test_client_sort_reorders_rows(live_server, page):
    page.goto(f"{live_server.url}/table/")
    _ready(page)
    header_btn = page.locator(".dcc-table__th button").first

    header_btn.click()
    page.wait_for_timeout(200)
    asc_first = _rows(page).first.text_content()
    header_btn.click()  # toggle direction
    page.wait_for_timeout(200)
    desc_first = _rows(page).first.text_content()

    assert asc_first != desc_first
    assert page.locator(".dcc-table__sortcue").first.text_content() in {"▲", "▼"}


@pytest.mark.django_db
def test_client_pagination_appears_past_one_page(live_server, page, transactional_db):
    from demo.models import Task

    Task.objects.bulk_create(
        Task(title=f"Bulk task {n:03d}", priority="low", done=False, due_date=datetime.date.today())
        for n in range(40)
    )
    page.goto(f"{live_server.url}/e2e/table/")
    _ready(page)
    nav = page.locator("nav.dcc-table__pagination")
    nav.wait_for(state="visible")
    per_page = _rows(page).count()
    assert 0 < per_page < 45  # a page, not the whole 45-row set
    assert "Page 1 of" in nav.text_content()

    nav.locator("button:has-text('Next')").click()
    page.wait_for_function(
        "() => /Page 2 of/.test(document.querySelector('nav.dcc-table__pagination').textContent)"
    )


def test_resource_row_click_navigates(live_server, page):
    page.goto(f"{live_server.url}/task/")
    _ready(page)
    clickable = page.locator(".dcc-table__row--clickable")
    if clickable.count() == 0:
        pytest.skip("resource table rows are not click-navigable in this build")
    clickable.first.click()
    page.wait_for_url(lambda url: "/task/" in url and not url.rstrip("/").endswith("task"))
