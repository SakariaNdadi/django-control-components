"""The governing invariant (plan § Verification-3):

    A studio-built page and a hand-coded page must render identical markup.

The studio is an authoring layer, never a parallel rendering stack — it writes
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
    """Phase 3b groundwork: an ``AppShell`` with no topbar/footer must produce
    the same frame as the hand-coded ``panels/base.html`` — ``<main
    class="dcc-panel__main">`` as a *direct* child of ``.dcc-panel``, with no
    ``.dcc-panel__body`` wrapper (that wrapper drops ``.dcc-panel__main``'s
    max-width). This is the parity check that gates swapping base.html over.
    """
    from django.template.loader import render_to_string

    from django_control_components.blocks import AppShell
    from django_control_components.panels import Panel

    panel = Panel("parity").path("parity")
    base = soup(
        render_to_string(
            "django_control_components/panels/base.html",
            {"panel": panel, "nav_tree": [], "resource_label": "X", "nav": []},
        )
    )
    base_panel = base.select_one(".dcc-panel")
    base_main = base_panel.select_one(":scope > main.dcc-panel__main")
    assert base_main is not None
    assert base.select_one(".dcc-panel__body") is None

    shell = soup(_render(AppShell.make().fill("content", [Divider.make()])))
    shell_panel = shell.select_one(".dcc-panel")
    assert shell_panel.select_one(":scope > main.dcc-panel__main") is not None
    assert shell.select_one(".dcc-panel__body") is None


def test_appshell_wraps_body_only_when_topbar_or_footer_present(soup):
    from django_control_components.blocks import AppShell, Footer

    with_footer = soup(
        _render(AppShell.make().fill("content", [Divider.make()]).fill("footer", [Footer.make()]))
    )
    body = with_footer.select_one(".dcc-panel > .dcc-panel__body")
    assert body is not None
    assert body.select_one("main.dcc-panel__main") is not None


def test_widget_parity_python_vs_spec():
    coded = StatWidget.make("Orders").value(42)
    coded._auto_id = "w0"

    (hydrated,) = build_widgets_from_spec(
        [{"type": "StatWidget", "name": "Orders", "config": {"value": 42}}]
    )
    hydrated._auto_id = "w0"

    assert _render(coded) == _render(hydrated)
