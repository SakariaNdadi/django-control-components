"""Navigation blocks - NavLink / NavGroup / NavHeading / NavDivider / NavUser
and the panel sidebar wiring."""

from __future__ import annotations

import pytest
from django.test import RequestFactory

from django_control_components.blocks import (
    NavAction,
    NavDivider,
    NavGroup,
    NavHeading,
    NavLink,
    NavUser,
    Sidebar,
    ThemeToggle,
)
from django_control_components.core.context import RenderContext

pytestmark = pytest.mark.django_db


def _ctx(path="/"):
    return RenderContext(request=RequestFactory().get(path))


def test_nav_link_renders_icon_badge_and_dot(soup):
    html = str(
        NavLink().label("Inbox").icon("inbox").to("/inbox/").badge("6").dot("#f00").render(_ctx())
    )
    doc = soup(html)
    a = doc.select_one("a.dcc-nav__link")
    assert a["href"] == "/inbox/"
    assert doc.select_one(".dcc-nav__badge").text.strip() == "6"
    assert "#f00" in doc.select_one(".dcc-nav__dot")["style"]


def test_nav_link_active_from_request_path(soup):
    on = soup(str(NavLink().label("Tasks").to("/tasks/").render(_ctx("/tasks/new/"))))
    off = soup(str(NavLink().label("Tasks").to("/tasks/").render(_ctx("/other/"))))
    assert "is-active" in on.select_one("a")["class"]
    assert on.select_one("a")["aria-current"] == "page"
    assert "is-active" not in off.select_one("a").get("class", [])


def test_nav_link_active_can_be_forced(soup):
    doc = soup(str(NavLink().label("Home").to("/").active(True).render(_ctx("/anything/"))))
    assert "is-active" in doc.select_one("a")["class"]


def test_nav_link_url_name_reverses_or_falls_back():
    html = str(NavLink().label("X").to("no-such-route-name").render(_ctx()))
    assert 'href="#"' in html  # NoReverseMatch -> "#"


def test_nav_group_is_collapsible_and_a11y(soup):
    group = (
        NavGroup().label("Reports").open().fill("default", [NavLink().label("Weekly").to("/w/")])
    )
    doc = soup(str(group.render(_ctx())))
    li = doc.select_one("li.dcc-nav__group")
    assert li["data-default-open"] == "1"
    assert "dccNav(" in li["x-data"]
    btn = doc.select_one("button.dcc-nav__grouptoggle")
    sub = doc.select_one("ul.dcc-nav__sublist")
    assert btn["aria-controls"] == sub["id"]
    assert sub["role"] == "group"
    assert doc.select_one("ul.dcc-nav__sublist a")["href"] == "/w/"


def test_nav_heading_and_divider(soup):
    assert "Projects" in str(NavHeading().label("Projects").render(_ctx()))
    assert "<hr" in str(NavDivider().render(_ctx()))
    assert "dcc-nav__action" in str(
        NavAction().label("Add").icon("plus").to("/new/").render(_ctx())
    )


def test_nav_user_card_and_menu(soup):
    doc = soup(
        str(
            NavUser()
            .label("Ada Lovelace")
            .email("ada@example.com")
            .menu([("Settings", "/settings/"), ("Sign out", "no-route")])
            .render(_ctx())
        )
    )
    assert "Ada Lovelace" in doc.select_one(".dcc-nav__usercard").text
    items = doc.select(".dcc-nav__usermenuitem")
    assert items[0]["href"] == "/settings/"
    assert items[1]["href"] == "#"  # unresolvable name
    assert doc.select_one('[role="menu"]') is not None


def test_sidebar_two_slots(soup):
    sb = (
        Sidebar()
        .brand("DCC")
        .fill("default", [NavLink().label("Home").to("/")])
        .fill("footer", [ThemeToggle()])
    )
    doc = soup(str(sb.render(_ctx())))
    assert doc.select_one("nav.dcc-panel__nav .dcc-panel__brand strong").text == "DCC"
    assert doc.select_one(".dcc-nav a")["href"] == "/"
    assert doc.select_one(".dcc-panel__navfoot .dcc-nav__theme") is not None


def test_theme_toggle_uses_shell_scope():
    html = str(ThemeToggle().render(_ctx()))
    assert "cycleTheme()" in html and "themeLabel()" in html


def test_panel_sidebar_groups_the_tree(soup, django_user_model):
    from django_control_components.panels import Panel
    from django_control_components.panels.nav import panel_sidebar
    from django_control_components.panels.resource import Resource
    from tests.testapp.models import Article

    class ArticleResource(Resource):
        model = Article
        navigation_group = "Content"

    panel = Panel("navb").path("navb").resources([ArticleResource])

    class _Conf:
        urlpatterns = [panel.mount()]

    import sys

    sys.modules[__name__ + "_urls"] = _Conf
    req = RequestFactory().get("/navb/article/")
    req.user = django_user_model.objects.create_superuser("nb", "nb@x.io", "x")

    from django.test import override_settings

    with override_settings(ROOT_URLCONF=__name__ + "_urls"):
        html = str(panel_sidebar(panel, req).render(RenderContext(request=req)))
    doc = soup(html)
    group = doc.select_one("li.dcc-nav__group")
    assert group is not None and "Content" in group.text
    # the active article link sits inside the (auto-opened) group
    assert group["data-default-open"] == "1"
    assert doc.select_one(".dcc-panel__navfoot .dcc-nav__theme") is not None
