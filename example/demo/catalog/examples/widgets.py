"""Catalog pages for ``django_control_components.panels`` dashboard widgets."""

from __future__ import annotations

from django_control_components.panels import BarListWidget, ChartWidget, StatWidget, TableWidget
from django_control_components.tables import BadgeColumn, Table, TextColumn

from ...models import Task
from ..page import ComponentExample, ComponentPageSpec


def _recent_task_table(request):
    return (
        Table.make(Task.objects.all())
        .id("demo-recent-tasks")
        .columns([TextColumn.make("title"), BadgeColumn.make("priority")])
        .client_side()
    )


STAT_WIDGET = ComponentPageSpec(
    slug="stat-widget",
    title="Stat Widget",
    family="widgets",
    icon="gauge-high",
    summary="A single labelled number.",
    examples=[
        ComponentExample(
            title="Basic",
            code=(
                'StatWidget.make("Tasks", lambda request: Task.objects.count())\n'
                '    .icon("list-check")'
            ),
            build=lambda request: StatWidget.make(
                "Tasks", lambda request: Task.objects.count()
            ).icon("list-check"),
        ),
    ],
)

CHART_WIDGET = ComponentPageSpec(
    slug="chart-widget",
    title="Chart Widget",
    family="widgets",
    icon="chart-column",
    summary="Chart.js-backed. .kind() picks line/bar/area/pie/doughnut/radar.",
    examples=[
        ComponentExample(
            title="Bar",
            code=(
                'ChartWidget.make("By priority").kind("bar")\n'
                '    .data([("Low", 2), ("Medium", 5), ("High", 1)])'
            ),
            build=lambda request: (
                ChartWidget.make("By priority")
                .kind("bar")
                .data([("Low", 2), ("Medium", 5), ("High", 1)])
            ),
        ),
    ],
)

BAR_LIST_WIDGET = ComponentPageSpec(
    slug="bar-list-widget",
    title="Bar List Widget",
    family="widgets",
    icon="chart-simple",
    summary="A dependency-free CSS bar chart. No JavaScript, no CDN.",
    examples=[
        ComponentExample(
            title="Basic",
            code='BarListWidget.make("By priority").data([("Low", 2), ("Medium", 5), ("High", 1)])',
            build=lambda request: BarListWidget.make("By priority").data(
                [("Low", 2), ("Medium", 5), ("High", 1)]
            ),
        ),
    ],
)

TABLE_WIDGET = ComponentPageSpec(
    slug="table-widget",
    title="Table Widget",
    family="widgets",
    icon="table",
    summary="Wraps a Table, keeping its own toolbar/pagination/refresh.",
    examples=[
        ComponentExample(
            title="Basic",
            code='TableWidget.make("Recent tasks", lambda r: recent_task_table(r))',
            build=lambda request: TableWidget.make("Recent tasks", _recent_task_table),
        ),
    ],
)

PAGES = [STAT_WIDGET, CHART_WIDGET, BAR_LIST_WIDGET, TABLE_WIDGET]
