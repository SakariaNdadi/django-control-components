"""Sidebar navigation: collapsible groups, persistence across a full-page
navigation, and the searchable filter."""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.e2e


def _ready(page):
    page.wait_for_selector(".dcc-nav__group")
    page.wait_for_function("window.Alpine && window.Alpine.version")


def test_group_toggles_and_persists_open_state(live_server, page):
    page.goto(f"{live_server.url}/e2e/nav/")
    _ready(page)
    beta = page.locator(".dcc-nav__group").nth(1)
    assert beta.locator(".dcc-nav__sublist").is_visible()

    beta.locator(".dcc-nav__grouptoggle").click()
    page.wait_for_function(
        "el => el.dataset.defaultOpen === '0'", arg=beta.element_handle(), timeout=5000
    )
    assert not beta.locator(".dcc-nav__sublist").is_visible()


def test_collapsed_group_reopens_after_navigation(live_server, page):
    """Regression: `dccNav.toggle()` must write `data-default-open` on the group
    `<li>` (via `$root`), not the button (`$el`), or the collapsed-from-paint CSS
    rule keeps the sublist hidden and the group is stuck shut."""
    page.goto(f"{live_server.url}/e2e/nav/")
    _ready(page)

    beta = page.locator(".dcc-nav__group").nth(1)
    beta.locator(".dcc-nav__grouptoggle").click()
    page.wait_for_function(
        "el => el.dataset.defaultOpen === '0'", arg=beta.element_handle(), timeout=5000
    )

    page.click(".dcc-nav__link[href='/e2e/nav/?p=2']")
    _ready(page)
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


def test_sidebar_filter_hides_non_matching_links(live_server, page):
    page.goto(f"{live_server.url}/e2e/nav/")
    _ready(page)
    page.fill(".dcc-nav__filter input", "Alpha two")
    page.wait_for_function(
        "() => [...document.querySelectorAll('.dcc-nav__item')]"
        ".filter(li => !li.hidden).every(li => /Alpha two/.test(li.textContent))"
    )
    visible = page.locator(".dcc-nav__item:visible")
    assert visible.count() == 1
    assert "Alpha two" in visible.first.text_content()

    page.fill(".dcc-nav__filter input", "")
    page.wait_for_function(
        "() => document.querySelectorAll('.dcc-nav__item:not([hidden])').length >= 3"
    )
