"""Panel widgets on the demo catalog: the Chart widget actually paints a
Chart.js canvas, the Stat / BarList / Table widgets render their shells."""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.e2e


def _ready(page):
    page.wait_for_function("window.Alpine && window.Alpine.version")


def test_chart_widget_paints_a_canvas(live_server, page):
    page.goto(f"{live_server.url}/chart-widget/")
    _ready(page)
    canvas = page.locator("canvas").first
    canvas.wait_for()
    # Chart.js sizes the canvas backing store once it has drawn
    page.wait_for_function(
        "() => { const c = document.querySelector('canvas');"
        " return c && c.width > 0 && c.getContext('2d'); }"
    )
    assert page.evaluate("!!window.Chart")


def test_stat_widget_renders(live_server, page):
    page.goto(f"{live_server.url}/stat-widget/")
    _ready(page)
    assert page.locator(".dcc-widget").first.is_visible()


def test_bar_list_widget_is_js_free(live_server, page):
    page.goto(f"{live_server.url}/bar-list-widget/")
    _ready(page)
    assert page.locator(".dcc-widget").first.is_visible()


def test_table_widget_embeds_a_table(live_server, page):
    page.goto(f"{live_server.url}/table-widget/")
    _ready(page)
    assert page.locator(".dcc-widget [x-data^='dccTable'], [x-data^='dccTable']").count() >= 1
    assert page.locator(".dcc-table__row").count() >= 1
