"""Exhaustive static smoke: every page reachable from the demo panel sidebar -
one live render of every catalog component, plus the resource / table / widget
pages - must return 200 and raise no severe console error or unhandled
exception in the browser.
"""

from __future__ import annotations

import re

import pytest

pytestmark = pytest.mark.e2e

_IGNORE = re.compile(
    r"favicon|/static/.*404|ResizeObserver|ERR_NETWORK_CHANGED|ERR_NETWORK_IO_SUSPENDED"
)


def _nav_links(page, base: str) -> list[str]:
    page.goto(base + "/")
    page.wait_for_selector(".dcc-nav__link")
    hrefs = page.eval_on_selector_all(
        ".dcc-nav__link", "els => els.map(e => e.getAttribute('href'))"
    )
    seen: list[str] = []
    for href in hrefs:
        if href and href.startswith("/") and href not in seen:
            seen.append(href)
    return seen


def test_every_catalog_page_renders_clean(live_server, page):
    errors: list[tuple[str, str]] = []
    current = {"url": "/"}
    page.on(
        "console",
        lambda m: (
            m.type == "error"
            and not _IGNORE.search(m.text)
            and errors.append((current["url"], m.text))
        ),
    )
    page.on(
        "pageerror",
        lambda e: not _IGNORE.search(str(e)) and errors.append((current["url"], str(e))),
    )

    links = _nav_links(page, live_server.url)
    assert len(links) > 30, f"expected the full catalog, got {len(links)} links"

    visited = 0
    for href in links:
        current["url"] = href
        resp = page.goto(live_server.url + href)
        assert resp is not None and resp.status < 400, f"{href} -> {resp and resp.status}"
        page.wait_for_selector("main, .dcc-panel__main, body")
        page.wait_for_timeout(120)
        visited += 1

    assert visited == len(links)
    assert not errors, "console errors:\n" + "\n".join(f"  {u}: {t}" for u, t in errors)
