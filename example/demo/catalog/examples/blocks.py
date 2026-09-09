"""Catalog pages for ``django_control_components.blocks`` layout/chrome."""

from __future__ import annotations

from django_control_components.blocks.chrome import Footer, Navbar, Sidebar
from django_control_components.blocks.layout import Card, Column, Divider, Grid, Row, Spacer, Stack

from ...blocks import Html
from ..page import ComponentExample, ComponentPageSpec


def _chip(text: str) -> Html:
    return Html().content(f'<span class="dcc-docs__chip">{text}</span>')


STACK = ComponentPageSpec(
    slug="stack",
    title="Stack",
    family="blocks",
    icon="bars",
    summary="Vertical flow.",
    examples=[
        ComponentExample(
            title="Basic",
            code=(
                'Stack.make().gap("sm").fill("default", [\n'
                '    Card.make().title("One"), Card.make().title("Two"),\n'
                "])"
            ),
            build=lambda request: (
                Stack.make()
                .gap("sm")
                .fill("default", [Card.make().title("One"), Card.make().title("Two")])
            ),
        ),
    ],
)

ROW = ComponentPageSpec(
    slug="row",
    title="Row",
    family="blocks",
    icon="grip-lines",
    summary="Horizontal flow with wrap/alignment/justification.",
    examples=[
        ComponentExample(
            title="Basic",
            code=(
                'Row.make().gap("sm").justify("between")\n'
                '    .fill("default", [chip_one, chip_two, chip_three])'
            ),
            build=lambda request: (
                Row.make()
                .gap("sm")
                .justify("between")
                .fill("default", [_chip("One"), _chip("Two"), _chip("Three")])
            ),
        ),
    ],
)

GRID = ComponentPageSpec(
    slug="grid-block",
    title="Grid (block)",
    family="blocks",
    icon="table-cells",
    summary="A CSS grid - cols tracks, gap spacing.",
    examples=[
        ComponentExample(
            title="Two columns",
            code=(
                'Grid.make().cols(2).gap("md").fill("default", [\n'
                '    Column.make().span(1).fill("default", []),\n'
                '    Column.make().span(1).fill("default", []),\n'
                "])"
            ),
            build=lambda request: (
                Grid.make()
                .cols(2)
                .gap("md")
                .fill(
                    "default",
                    [
                        Column.make().span(1).fill("default", [_chip("Left")]),
                        Column.make().span(1).fill("default", [_chip("Right")]),
                    ],
                )
            ),
        ),
    ],
)

CARD = ComponentPageSpec(
    slug="card",
    title="Card",
    family="blocks",
    icon="square",
    summary="A bordered surface with optional header and footer slots.",
    examples=[
        ComponentExample(
            title="Basic",
            code='Card.make().title("Summary").fill("body", [text])',
            build=lambda request: (
                Card.make()
                .title("Summary")
                .fill("body", [Html().content("<p>Three tasks are overdue this week.</p>")])
            ),
        ),
    ],
)

DIVIDER = ComponentPageSpec(
    slug="divider",
    title="Divider",
    family="blocks",
    icon="minus",
    summary="A horizontal rule. No children.",
    examples=[
        ComponentExample(
            title="Basic",
            code="Divider.make()",
            build=lambda request: Card.make().fill("body", [Divider.make()]),
        ),
    ],
)

SPACER = ComponentPageSpec(
    slug="spacer",
    title="Spacer",
    family="blocks",
    icon="arrows-up-down",
    summary="Fixed vertical whitespace.",
    examples=[
        ComponentExample(
            title="Basic",
            code='Spacer.make().size("lg")',
            build=lambda request: Card.make().fill("body", [Spacer.make().size("lg")]),
        ),
    ],
)

NAVBAR = ComponentPageSpec(
    slug="navbar",
    title="Navbar",
    family="blocks",
    icon="window-maximize",
    summary="A horizontal bar with a leading and a trailing region.",
    examples=[
        ComponentExample(
            title="Basic",
            code='Navbar.make().brand("DCC").fill("end", [chip])',
            build=lambda request: Navbar.make().brand("DCC").fill("end", [_chip("v0.0.1")]),
        ),
    ],
)

SIDEBAR = ComponentPageSpec(
    slug="sidebar",
    title="Sidebar",
    family="blocks",
    icon="table-columns",
    summary="A vertical nav column.",
    examples=[
        ComponentExample(
            title="Basic",
            code='Sidebar.make().brand("DCC").brand_icon("cubes").fill("default", [links])',
            build=lambda request: (
                Sidebar.make()
                .brand("DCC")
                .brand_icon("cubes")
                .fill(
                    "default",
                    [
                        Html().content(
                            '<a class="dcc-nav__link is-active">Dashboard</a>'
                            '<a class="dcc-nav__link">Tasks</a>'
                        )
                    ],
                )
            ),
        ),
    ],
)

FOOTER = ComponentPageSpec(
    slug="footer",
    title="Footer",
    family="blocks",
    icon="grip-lines",
    summary="A page footer.",
    examples=[
        ComponentExample(
            title="Basic",
            code='Footer.make().fill("default", [text])',
            build=lambda request: Footer.make().fill(
                "default", [Html().content("<p>&copy; DCC</p>")]
            ),
        ),
    ],
)

PAGES = [STACK, ROW, GRID, CARD, DIVIDER, SPACER, NAVBAR, SIDEBAR, FOOTER]
