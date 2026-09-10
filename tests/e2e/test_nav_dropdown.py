"""Regression: a sidebar group the viewer collapsed must still re-open after a
full-page navigation.

`dccNav` mirrors the open state onto `data-default-open` on the group `<li>`; the
`.dcc-nav__group[data-default-open="0"] > .dcc-nav__sublist { display: none }`
rule collapses it from first paint. If `toggle()` writes the attribute on the
wrong element (the button, via `$el`, instead of the `<li>`, via `$root`) the
rule keeps winning and the group can never be expanded again.
"""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.e2e


def _wait_ready(page):
    page.wait_for_selector(".dcc-nav__group")
    page.wait_for_function("window.Alpine && window.Alpine.version")


def test_collapsed_group_reopens_after_navigation(live_server, page):
    page.goto(f"{live_server.url}/e2e/nav/")
    _wait_ready(page)

    beta = page.locator(".dcc-nav__group").nth(1)
    beta.locator(".dcc-nav__grouptoggle").click()
    page.wait_for_function(
        "el => el.dataset.defaultOpen === '0'", arg=beta.element_handle(), timeout=5000
    )

    # full-page navigation - the server now renders Beta collapsed from the cookie
    page.click(".dcc-nav__link[href='/e2e/nav/?p=2']")
    _wait_ready(page)
    page.wait_for_selector("#page-marker:has-text('page 2')")

    beta = page.locator(".dcc-nav__group").nth(1)
    assert beta.get_attribute("data-default-open") == "0"
    sublist = beta.locator(".dcc-nav__sublist")
    assert not sublist.is_visible()

    beta.locator(".dcc-nav__grouptoggle").click()
    page.wait_for_function(
        "el => el.dataset.defaultOpen === '1'", arg=beta.element_handle(), timeout=5000
    )
    assert sublist.is_visible()
