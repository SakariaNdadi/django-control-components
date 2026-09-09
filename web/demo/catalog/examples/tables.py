"""Catalog pages for ``django_control_components.tables`` columns/filters."""

from __future__ import annotations

from django_control_components.actions import Action
from django_control_components.tables import (
    BadgeColumn,
    BooleanColumn,
    BooleanFilter,
    DateColumn,
    ImageColumn,
    SelectFilter,
    Table,
    TernaryFilter,
    TextColumn,
)

from ...models import Task
from ..page import ComponentExample, ComponentPageSpec, demo_authorize


def _mark_done(record):
    record.done = True
    record.save(update_fields=["done"])


def _demo_table(request, columns, filters=None):
    table = (
        Table.make(Task.objects.all()).id(f"demo-{columns[0].name}").columns(columns).client_side()
    )
    if filters:
        table.filters(filters)
    return table


TABLE = ComponentPageSpec(
    slug="table",
    title="Table",
    family="tables",
    icon="table",
    summary=(
        "The full builder: columns, filters, a row action, keyset streaming "
        "and search picked automatically by row count."
    ),
    examples=[
        ComponentExample(
            title="Full example",
            code=(
                "Table.make(Task.objects.all())\n"
                '    .id("catalog-tasks")\n'
                "    .columns([\n"
                '        TextColumn.make("title").sortable().searchable(),\n'
                '        BadgeColumn.make("priority").colors({"high": "danger"}),\n'
                '        BooleanColumn.make("done").labels(("✓", "-")),\n'
                '        DateColumn.make("due_date").since(),\n'
                "    ])\n"
                '    .filters([SelectFilter.make("priority").options(Task.Priority.choices)])\n'
                '    .actions([Action.make("mark_done").icon("check").action(...)])\n'
                '    .default_sort("-due_date")\n'
                "    .searchable()"
            ),
            build=lambda request: (
                Table.make(Task.objects.all())
                .id("catalog-tasks")
                .columns(
                    [
                        TextColumn.make("title").sortable().searchable(),
                        BadgeColumn.make("priority").colors(
                            {"low": "muted", "medium": "secondary", "high": "danger"}
                        ),
                        BooleanColumn.make("done").labels(("✓", "-")),
                        DateColumn.make("due_date").since(),
                    ]
                )
                .filters([SelectFilter.make("priority").options(Task.Priority.choices)])
                .actions(
                    [
                        Action.make("mark_done")
                        .icon("check")
                        .action(_mark_done)
                        .authorize(demo_authorize)
                    ]
                )
                .default_sort("-due_date")
                .searchable()
            ),
        ),
    ],
    props_table=[
        (".id(str)", "str", "stable id; the ?_dcc_table=<id> fragment handle"),
        (".columns([...])", "list[Column]", ""),
        (".filters([...])", "list[Filter]", ""),
        (".actions([...])", "list[Action]", "one button per action in a trailing column"),
        (".bulk_actions([...])", "list[BulkAction]", "leading checkbox column + toolbar"),
        (".searchable(bool=True)", "bool", "auto-on if any column is .searchable()"),
        (".default_sort(str)", "str", "- prefix = descending"),
        (".stream() / .page_numbers()", "-", "keyset cursor vs classic COUNT(*) pages"),
        (".client_side() / .server_side()", "-", "force the render mode"),
        (
            ".with_related(bool=True)",
            "bool",
            "auto select_related / prefetch_related from dotted column names (on by default)",
        ),
    ],
)

TEXT_COLUMN = ComponentPageSpec(
    slug="text-column",
    title="Text Column",
    family="tables",
    icon="font",
    summary="The value, escaped. `name` may be dotted (`\"author.name\"`).",
    examples=[
        ComponentExample(
            title="Basic",
            code='TextColumn.make("title").sortable().searchable().limit(64)',
            build=lambda request: _demo_table(
                request, [TextColumn.make("title").sortable().searchable().limit(64)]
            ),
            note=(
                "A dotted name walks a relation - `TextColumn.make(\"author.name\")`. "
                "The table adds `author` to `select_related` automatically so it "
                "stays one query; `.with_related(False)` opts out."
            ),
        ),
    ],
)

BADGE_COLUMN = ComponentPageSpec(
    slug="badge-column",
    title="Badge Column",
    family="tables",
    icon="tag",
    summary="A dcc-badge pill. .colors({value: variant}) maps the value to a variant.",
    examples=[
        ComponentExample(
            title="Basic",
            code=(
                'BadgeColumn.make("priority").colors('
                '{"low": "muted", "medium": "secondary", "high": "danger"})'
            ),
            build=lambda request: _demo_table(
                request,
                [
                    TextColumn.make("title"),
                    BadgeColumn.make("priority").colors(
                        {"low": "muted", "medium": "secondary", "high": "danger"}
                    ),
                ],
            ),
        ),
    ],
)

BOOLEAN_COLUMN = ComponentPageSpec(
    slug="boolean-column",
    title="Boolean Column",
    family="tables",
    icon="check",
    summary='.labels(("yes", "no")) -> a dcc-badge pill; default ("Yes", "No").',
    examples=[
        ComponentExample(
            title="Basic",
            code='BooleanColumn.make("done").labels(("✓", "-"))',
            build=lambda request: _demo_table(
                request, [TextColumn.make("title"), BooleanColumn.make("done").labels(("✓", "-"))]
            ),
        ),
    ],
)

DATE_COLUMN = ComponentPageSpec(
    slug="date-column",
    title="Date Column",
    family="tables",
    icon="calendar",
    summary='.since() -> "3 days ago"; else .date_format("N j, Y").',
    examples=[
        ComponentExample(
            title="Relative",
            code='DateColumn.make("due_date").since()',
            build=lambda request: _demo_table(
                request, [TextColumn.make("title"), DateColumn.make("due_date").since()]
            ),
        ),
    ],
)

IMAGE_COLUMN = ComponentPageSpec(
    slug="image-column",
    title="Image Column",
    family="tables",
    icon="image",
    summary=".thumbnail((w, h)), .rounded() -> an <img> from an ImageField.",
    examples=[
        ComponentExample(
            title="Basic",
            code='ImageColumn.make("cover").thumbnail((40, 40)).rounded()',
            build=lambda request: _demo_table(
                request,
                [
                    ImageColumn.make("cover").thumbnail((40, 40)).rounded(),
                    TextColumn.make("title"),
                    BadgeColumn.make("priority").colors(
                        {"low": "muted", "medium": "secondary", "high": "danger"}
                    ),
                ],
            ),
        ),
    ],
)

SELECT_FILTER = ComponentPageSpec(
    slug="select-filter",
    title="Select Filter",
    family="tables",
    icon="filter",
    summary="A value not in the option set is ignored.",
    examples=[
        ComponentExample(
            title="Basic",
            code='SelectFilter.make("priority").options(Task.Priority.choices)',
            build=lambda request: _demo_table(
                request,
                [TextColumn.make("title"), BadgeColumn.make("priority")],
                filters=[SelectFilter.make("priority").options(Task.Priority.choices)],
            ),
        ),
    ],
)

BOOLEAN_FILTER = ComponentPageSpec(
    slug="boolean-filter",
    title="Boolean Filter",
    family="tables",
    icon="filter",
    summary='"true"->True, "false"->False, anything else ignored.',
    examples=[
        ComponentExample(
            title="Basic",
            code='BooleanFilter.make("done")',
            build=lambda request: _demo_table(
                request,
                [TextColumn.make("title"), BooleanColumn.make("done")],
                filters=[BooleanFilter.make("done")],
            ),
        ),
    ],
)

TERNARY_FILTER = ComponentPageSpec(
    slug="ternary-filter",
    title="Ternary Filter",
    family="tables",
    icon="filter",
    summary="BooleanFilter with All / Yes / No choices.",
    examples=[
        ComponentExample(
            title="Basic",
            code='TernaryFilter.make("done")',
            build=lambda request: _demo_table(
                request,
                [TextColumn.make("title"), BooleanColumn.make("done")],
                filters=[TernaryFilter.make("done")],
            ),
        ),
    ],
)

PAGES = [
    TABLE,
    TEXT_COLUMN,
    BADGE_COLUMN,
    BOOLEAN_COLUMN,
    DATE_COLUMN,
    IMAGE_COLUMN,
    SELECT_FILTER,
    BOOLEAN_FILTER,
    TERNARY_FILTER,
]
