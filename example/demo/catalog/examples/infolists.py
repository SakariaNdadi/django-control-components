"""Catalog pages for ``django_control_components.infolists`` entries."""

from __future__ import annotations

from types import SimpleNamespace

from django_control_components.infolists import (
    BadgeEntry,
    BooleanEntry,
    DateEntry,
    Infolist,
    TextEntry,
)

from ..page import ComponentExample, ComponentPageSpec

_RECORD = SimpleNamespace(title="Ship the release", priority="high", done=False, due_date=None)


def _infolist(request, entries):
    return Infolist.make().schema(entries).render(request=request, record=_RECORD)


TEXT_ENTRY = ComponentPageSpec(
    slug="text-entry",
    title="Text Entry",
    family="infolists",
    icon="font",
    summary='The value; "-" (or .placeholder(...)) when None/"".',
    examples=[
        ComponentExample(
            title="Basic",
            code='TextEntry.make("title")',
            build=lambda request: _infolist(request, [TextEntry.make("title")]),
        ),
    ],
)

BADGE_ENTRY = ComponentPageSpec(
    slug="badge-entry",
    title="Badge Entry",
    family="infolists",
    icon="tag",
    summary="A dcc-badge pill. .colors({value: variant}) maps the value to a variant.",
    examples=[
        ComponentExample(
            title="Basic",
            code='BadgeEntry.make("priority").colors({"high": "danger", "low": "muted"})',
            build=lambda request: _infolist(
                request, [BadgeEntry.make("priority").colors({"high": "danger", "low": "muted"})]
            ),
        ),
    ],
)

BOOLEAN_ENTRY = ComponentPageSpec(
    slug="boolean-entry",
    title="Boolean Entry",
    family="infolists",
    icon="check",
    summary="Yes / No badge (No is unstyled, Yes is success).",
    examples=[
        ComponentExample(
            title="Basic",
            code='BooleanEntry.make("done")',
            build=lambda request: _infolist(request, [BooleanEntry.make("done")]),
        ),
    ],
)

DATE_ENTRY = ComponentPageSpec(
    slug="date-entry",
    title="Date Entry",
    family="infolists",
    icon="calendar",
    summary='.since() -> "3 days ago"; else .date_format(fmt) (default).',
    examples=[
        ComponentExample(
            title="Basic",
            code='DateEntry.make("due_date")',
            build=lambda request: _infolist(request, [DateEntry.make("due_date")]),
        ),
    ],
)

PAGES = [TEXT_ENTRY, BADGE_ENTRY, BOOLEAN_ENTRY, DATE_ENTRY]
