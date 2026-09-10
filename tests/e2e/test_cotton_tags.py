"""Every shipped ``<c-dcc.*>`` cotton tag, used in a real template and asserted
in the browser: correct DOM, classes, and (for the modal) working Alpine."""

from __future__ import annotations

import re

import pytest

pytestmark = pytest.mark.e2e

# transient sandbox network blips, not page defects
_NOISE = re.compile(r"ERR_NETWORK_CHANGED|ERR_NETWORK_IO_SUSPENDED|favicon")


@pytest.fixture
def cotton(live_server, page):
    page.goto(f"{live_server.url}/e2e/cotton/")
    page.wait_for_function("window.Alpine && window.Alpine.version")
    return page


def test_button_tag_variants_and_element(cotton):
    btns = cotton.locator("#buttons .dcc-btn")
    assert btns.count() == 8
    assert cotton.locator("#buttons button.dcc-btn--primary").count() >= 1
    assert cotton.locator("#buttons .dcc-btn--danger").is_visible()
    assert cotton.locator("#buttons .dcc-btn--sm").is_visible()
    # icon variant renders an <svg>/<i> inside
    assert (
        cotton.locator(
            "#buttons .dcc-btn:has-text('Icon') svg, #buttons .dcc-btn:has-text('Icon') i"
        ).count()
        >= 1
    )
    # disabled
    assert cotton.locator("#buttons button.dcc-btn:has-text('Disabled')").is_disabled()
    # href -> <a>
    link = cotton.locator("#buttons a.dcc-btn")
    assert link.get_attribute("href") == "/e2e/cotton/?x=1"
    assert cotton.locator("#buttons button[type='submit']").count() == 1


def test_badge_tag(cotton):
    badges = cotton.locator("#badges .dcc-badge")
    assert badges.count() == 3
    assert cotton.locator("#badges .dcc-badge--success").text_content().strip() == "Live"
    assert cotton.locator("#badges .dcc-badge--danger").is_visible()


def test_heading_tag_levels(cotton):
    assert cotton.locator("h1.dcc-heading").text_content().strip() == "Cotton tags"
    assert cotton.locator("#headings h2.dcc-heading").is_visible()
    assert cotton.locator("#headings h3.dcc-heading").is_visible()


def test_modal_tag_opens_and_closes(cotton):
    cotton.click("#modal button:has-text('Open cotton modal')")
    dialog = cotton.locator(".dcc-modal__dialog")
    dialog.wait_for(state="visible")
    assert cotton.locator("#cotton-modal-body").is_visible()
    cotton.click(".dcc-modal__body button:has-text('Dismiss')")
    dialog.wait_for(state="hidden")


def test_form_field_tags_render(cotton):
    assert cotton.locator("input#f-email[type='email'][required]").is_visible()
    assert cotton.locator("textarea#f-bio").is_visible()
    assert cotton.locator("input#f-pw[type='password']").is_visible()
    assert (
        cotton.locator("#f-agree input[type='checkbox'], input#f-agree[type='checkbox']").count()
        >= 1
    )
    assert cotton.locator(".dcc-field:has(#f-plan) input[type='radio']").count() == 2
    assert cotton.locator("#f-status").is_visible()
    assert cotton.locator("select#f-status option").count() >= 3
    assert cotton.locator("#f-tags").get_attribute("multiple") is not None
    assert cotton.locator("input#f-cover[type='file']").count() == 1


def test_cotton_page_has_no_console_errors(live_server, page):
    errors: list[str] = []
    page.on(
        "console",
        lambda m: m.type == "error" and not _NOISE.search(m.text) and errors.append(m.text),
    )
    page.on("pageerror", lambda e: not _NOISE.search(str(e)) and errors.append(str(e)))
    page.goto(f"{live_server.url}/e2e/cotton/")
    page.wait_for_function("window.Alpine && window.Alpine.version")
    page.wait_for_timeout(200)
    assert not errors, errors
