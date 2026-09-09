"""The governing invariant (plan § Verification-3):

    A studio-built page and a hand-coded page must render identical markup.

The studio is an authoring layer, never a parallel rendering stack - it writes
JSON that the same builders turn into the same components a dev would have
written in Python. These tests build a UI both ways and diff the HTML.
"""

from __future__ import annotations

import pytest

from django_control_components.blocks import Card, Column, Divider, Grid, Stack
from django_control_components.core.context import RenderContext
from django_control_components.panels import StatWidget
from django_control_components.studio.deserialize import (
    build_block_tree_from_spec,
    build_widgets_from_spec,
)

pytestmark = pytest.mark.django_db


def _render(component) -> str:
    return str(component.render(RenderContext(request=None)))


def test_block_tree_parity_python_vs_spec():
    coded = (
        Grid.make()
        .cols(6)
        .fill(
            "default",
            [
                Column.make()
                .span(3)
                .fill("default", [Card.make().title("Stats").fill("body", [Divider.make()])]),
                Column.make().span(3).fill("default", [Stack.make().gap("lg")]),
            ],
        )
    )

    spec = {
        "schema_version": 0,
        "root": {
            "type": "Grid",
            "props": {"cols": 6},
            "slots": {
                "default": [
                    {
                        "type": "Column",
                        "props": {"span": 3},
                        "slots": {
                            "default": [
                                {
                                    "type": "Card",
                                    "props": {"title": "Stats"},
                                    "slots": {
                                        "body": [{"type": "Divider", "props": {}, "slots": {}}]
                                    },
                                }
                            ]
                        },
                    },
                    {
                        "type": "Column",
                        "props": {"span": 3},
                        "slots": {
                            "default": [{"type": "Stack", "props": {"gap": "lg"}, "slots": {}}]
                        },
                    },
                ]
            },
        },
    }
    hydrated = build_block_tree_from_spec(spec)

    assert _render(coded) == _render(hydrated)


def test_appshell_default_shell_matches_panels_base_html(soup):
    """An ``AppShell`` must produce the same frame as the hand-coded
    ``panels/base.html``: ``.dcc-panel > .dcc-panel__body > main.dcc-panel__main``.
    The ``.dcc-panel__body`` flex column carries the topbar (when present) above
    ``<main>`` and the ``min-width: 0`` that lets the content column reflow when
    the sidebar rails.
    """
    from django.template.loader import render_to_string

    from django_control_components.blocks import AppShell
    from django_control_components.panels import Panel

    panel = Panel("parity").path("parity")
    from django.test import RequestFactory

    from django_control_components.panels.nav import sidebar_from_tree

    request = RequestFactory().get("/parity/")
    request.user = None
    base = soup(
        render_to_string(
            "django_control_components/panels/base.html",
            {
                "panel": panel,
                "nav_tree": [],
                "sidebar": sidebar_from_tree(panel, [], request, footer=False),
                "resource_label": "X",
                "nav": [],
            },
        )
    )
    base_main = base.select_one(".dcc-panel > .dcc-panel__body > main.dcc-panel__main")
    assert base_main is not None

    shell = soup(_render(AppShell.make().fill("content", [Divider.make()])))
    assert shell.select_one(".dcc-panel > .dcc-panel__body > main.dcc-panel__main") is not None


def test_appshell_body_holds_topbar_above_main_and_footer_below(soup):
    from django_control_components.blocks import AppShell, Footer, Navbar

    dom = soup(
        _render(
            AppShell.make()
            .fill("topbar", [Navbar.make()])
            .fill("content", [Divider.make()])
            .fill("footer", [Footer.make()])
        )
    )
    body = dom.select_one(".dcc-panel > .dcc-panel__body")
    assert body is not None
    order = [set(c.get("class", [])) | {c.name} for c in body.find_all(recursive=False)]

    def pos(marker):
        return next(i for i, s in enumerate(order) if marker in s)

    assert pos("dcc-navbar") < pos("dcc-panel__main") < pos("dcc-footer")


def test_widget_parity_python_vs_spec():
    coded = StatWidget.make("Orders").value(42)
    coded._auto_id = "w0"

    (hydrated,) = build_widgets_from_spec(
        [{"type": "StatWidget", "name": "Orders", "config": {"value": 42}}]
    )
    hydrated._auto_id = "w0"

    assert _render(coded) == _render(hydrated)
