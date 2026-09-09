"""Catalog pages for the navigation blocks - each renders a small live Sidebar."""

from __future__ import annotations

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

from django.templatetags.static import static

from ..page import ComponentExample, ComponentPageSpec

_LOGO = static("demo/logo.svg")


def _sidebar(*children, footer=None):
    sb = Sidebar().brand("DCC").fill("default", list(children))
    if footer:
        sb.fill("footer", footer)
    return sb


NAV_LINK = ComponentPageSpec(
    slug="nav-link",
    title="Nav Link",
    family="nav",
    icon="link",
    summary="One entry - icon, label, an optional count badge or colour dot.",
    examples=[
        ComponentExample(
            title="Basic",
            code=(
                'NavLink().label("Inbox").icon("inbox").to("/inbox/").badge("6")\n'
                'NavLink().label("Flowbite library").dot("#2563eb").to("/p/1/")'
            ),
            build=lambda request: _sidebar(
                NavLink().label("Home").icon("house").to("/").active(True),
                NavLink().label("Inbox").icon("inbox").to("/inbox/").badge("6"),
                NavLink().label("Reporting").icon("chart-line").to("/reporting/"),
                NavDivider(),
                NavHeading().label("Projects"),
                NavLink().label("Flowbite library").dot("#2563eb").to("/p/1/"),
                NavLink().label("Iconscale").dot("#7c3aed").to("/p/2/"),
                NavAction().label("Add new project").icon("plus").to("/p/new/"),
            ),
        ),
        ComponentExample(
            title="Image instead of icon",
            code=(
                'Sidebar().brand("DCC").brand_image("/static/demo/logo.svg")\n'
                'NavLink().label("Acme Corp").image("/static/demo/logo.svg").to("/o/acme/")'
            ),
            build=lambda request: Sidebar()
            .brand("DCC")
            .brand_image(_LOGO)
            .fill(
                "default",
                [
                    NavLink().label("Dashboard").icon("gauge").to("/").active(True),
                    NavHeading().label("Organisations"),
                    NavLink().label("Acme Corp").image(_LOGO).image_alt("Acme").to("/o/acme/"),
                    NavLink().label("Globex").image(_LOGO).image_alt("Globex").to("/o/globex/"),
                ],
            ),
        ),
    ],
    props_table=[
        (".label(str)", "str", ""),
        (".icon(name)", "str", "leading icon"),
        (".image(url) / .image_alt(str)", "str", "logo/avatar in place of the icon"),
        (".to(url | url_name)", "str", "path, #anchor, or a URL name"),
        (".badge(str)", "str", "trailing count pill"),
        (".dot(css_color)", "str", "leading colour square"),
        (".active(bool) / .active_for(prefix)", "-", "force / derive the active state"),
    ],
)

NAV_GROUP = ComponentPageSpec(
    slug="nav-group",
    title="Nav Group",
    family="nav",
    icon="folder-tree",
    summary="A collapsible section. `dccNav` remembers open/closed per group.",
    examples=[
        ComponentExample(
            title="Basic",
            code=(
                'NavGroup().label("My Tasks").icon("list-check").open().fill("default", [\n'
                '    NavLink().label("Today").to("/t/today/"),\n'
                '    NavLink().label("Upcoming").to("/t/next/"),\n'
                "])"
            ),
            build=lambda request: _sidebar(
                NavLink().label("Home").icon("house").to("/"),
                NavGroup()
                .label("My Tasks")
                .icon("list-check")
                .open()
                .fill(
                    "default",
                    [
                        NavLink().label("Today").to("/t/today/"),
                        NavLink().label("Upcoming").to("/t/next/"),
                    ],
                ),
                NavGroup()
                .label("Reporting")
                .icon("chart-line")
                .fill(
                    "default",
                    [
                        NavLink().label("Overview").to("/r/"),
                        NavLink().label("Exports").to("/r/exports/"),
                    ],
                ),
            ),
        ),
    ],
)

NAV_USER = ComponentPageSpec(
    slug="nav-user",
    title="Nav User",
    family="nav",
    icon="user",
    summary="An account card for the sidebar footer, with an optional menu.",
    examples=[
        ComponentExample(
            title="Basic",
            code=(
                'Sidebar().fill("footer", [\n'
                "    ThemeToggle(),\n"
                '    NavUser().label("Bonnie Green").email("bonnie@example.com")\n'
                '        .menu([("Settings", "/settings/"), ("Sign out", "/logout/")]),\n'
                "])"
            ),
            build=lambda request: _sidebar(
                NavLink().label("Home").icon("house").to("/"),
                NavLink().label("Settings").icon("gear").to("/settings/"),
                footer=[
                    ThemeToggle(),
                    NavUser()
                    .label("Bonnie Green")
                    .email("bonnie@example.com")
                    .menu([("Settings", "/settings/"), ("Sign out", "/logout/")]),
                ],
            ),
        ),
    ],
)

PAGES = [NAV_LINK, NAV_GROUP, NAV_USER]
