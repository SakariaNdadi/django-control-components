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


def test_nav_link_image_replaces_icon(soup):
    html = str(
        NavLink()
        .label("Acme")
        .icon("inbox")
        .image("/static/logo.png")
        .image_alt("Acme")
        .to("/a/")
        .render(_ctx())
    )
    doc = soup(html)
    img = doc.select_one("a.dcc-nav__link img.dcc-nav__img")
    assert img["src"] == "/static/logo.png"
    assert img["alt"] == "Acme"
    assert doc.select_one(".dcc-nav__icon") is None  # image wins over icon


def test_nav_group_image_replaces_icon(soup):
    html = str(NavGroup().label("Team").image("/l.svg").render(_ctx()))
    assert 'class="dcc-nav__img" src="/l.svg"' in html


def test_sidebar_brand_image(soup):
    doc = soup(
        str(
            Sidebar()
            .brand("DCC")
            .brand_icon("cube")
            .brand_image("/brand.png")
            .fill("default", [NavLink().label("H").to("/")])
            .render(_ctx())
        )
    )
    assert doc.select_one(".dcc-panel__brand img.dcc-panel__brandimg")["src"] == "/brand.png"


def test_page_shell_padding_and_margin(soup):
    from django_control_components.blocks import PageShell

    shell = PageShell().title("X").padding("2rem", left="4rem").margin(top="1rem")
    style = soup(str(shell.render(_ctx()))).select_one(".dcc-page")["style"]
    assert "padding-top:2rem" in style
    assert "padding-left:4rem" in style
    assert "margin-top:1rem" in style


def test_page_shell_padding_rejects_unsafe_value(soup):
    from django_control_components.blocks import PageShell

    shell = PageShell().title("X").padding('2rem;color:red}body{')
    node = soup(str(shell.render(_ctx()))).select_one(".dcc-page")
    assert node.get("style") in (None, "")


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


def test_panel_content_spacing_style():
    from django_control_components.panels import Panel

    panel = Panel("sp").content_spacing(padding={"top": "1rem", "left": "3rem"}, margin="0 auto")
    assert "padding-top:1rem" in panel.content_style
    assert "padding-left:3rem" in panel.content_style
    assert "margin-top:0 auto" in panel.content_style


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


def test_page_shell_generates_header_and_body(soup):
    from django_control_components.blocks import PageShell, Prose

    shell = (
        PageShell()
        .eyebrow("Tables")
        .title("Badge Column")
        .summary("A pill.")
        .accent("#b45309")
        .fill("content", [Prose().html("<p>hi</p>")])
    )
    doc = soup(str(shell.render(_ctx())))
    assert doc.select_one(".dcc-page__eyebrow").text == "Tables"
    assert doc.select_one("h1.dcc-page__title").text == "Badge Column"
    assert "--dcc-page-accent:#b45309" in doc.select_one(".dcc-page__header")["style"]
    assert doc.select_one(".dcc-page__body .dcc-prose p").text == "hi"


def test_page_shell_header_slot_overrides_generated(soup):
    from django_control_components.blocks import Divider, PageShell

    shell = PageShell().title("X").fill("header", [Divider()]).fill("content", [Divider()])
    doc = soup(str(shell.render(_ctx())))
    assert doc.select_one("h1.dcc-page__title") is None
    assert doc.select_one(".dcc-page__body") is not None


def test_prose_html_is_code_only():
    from django_control_components.core.describe import CODE_ONLY_SETTERS

    assert "html" in CODE_ONLY_SETTERS


def test_nav_group_sublist_has_no_x_cloak(soup):
    # progressive enhancement: the sublist renders visible; Alpine collapses
    # closed groups. x-cloak would hide it forever if Alpine never loads.
    html = str(
        NavGroup().label("G").fill("default", [NavLink().label("a").to("/a/")]).render(_ctx())
    )
    assert "dcc-nav__sublist" in html
    assert "x-cloak" not in html.split("dcc-nav__sublist", 1)[1].split(">", 1)[0]


def test_panel_sidebar_starts_every_group_open(soup, django_user_model):
    from django_control_components.panels import Panel
    from django_control_components.panels.nav import panel_sidebar
    from django_control_components.panels.resource import Resource
    from tests.testapp.models import Article

    class R(Resource):
        model = Article
        navigation_group = "Content"

    panel = Panel("navo").path("navo").resources([R])

    class _C:
        urlpatterns = [panel.mount()]

    import sys

    sys.modules[__name__ + "_o"] = _C
    req = RequestFactory().get("/navo/article/")
    req.user = django_user_model.objects.create_superuser("no", "no@x.io", "x")
    from django.test import override_settings

    with override_settings(ROOT_URLCONF=__name__ + "_o"):
        doc = soup(str(panel_sidebar(panel, req).render(RenderContext(request=req))))
    groups = doc.select("li.dcc-nav__group")
    assert groups and all(g["data-default-open"] == "1" for g in groups)
