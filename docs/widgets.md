# Widgets

Widgets are the blocks on a panel dashboard. Each one renders a persistent shell
(`<div class="dcc-widget" id="…">`) around a swappable content fragment
(`#<id>-content`). `.poll()` / `.refresh_on()` make the shell re-fetch just that
fragment over htmx, so a chart repaints without a full page load.

Compose them in `DashboardPage.widgets(request)`:

```python
from django_control_components.panels import (
    BarListWidget,
    ChartWidget,
    DashboardPage,
    StatWidget,
    TableWidget,
)


class Overview(DashboardPage):
    page_title = "Overview"

    def widgets(self, request):
        return [
            StatWidget.make("Tasks", lambda request: Task.objects.count()).icon("list-check"),
            StatWidget.make(
                "Open", lambda request: Task.objects.filter(done=False).count()
            )
            .icon("circle-dot")
            .poll(30),
            ChartWidget.make("By priority")
            .kind("bar")
            .data([("Low", 2), ("Medium", 5), ("High", 1)])
            .columns(2),
            BarListWidget.make("By priority").data([("Low", 2), ("Medium", 5), ("High", 1)]),
            TableWidget.make("Recent tasks", _recent_task_table),
        ]
```

This is `web/demo/catalog/examples/widgets.py` (`Task` = `web/demo/models.py`),
live at `/stat-widget/`, `/chart-widget/`, `/bar-list-widget/`, `/table-widget/`.

## Shared API

Every widget:

| method | effect |
| --- | --- |
| `.make(*args, **kwargs)` | construct; keyword args are applied as setters |
| `.id(str)` | stable id - the `?_dcc_widget=<id>` refresh handle and json_script id. Auto-assigned `w0`, `w1`, … when unset |
| `.columns(n)` | grid span (stat 1, chart/bar-list 2, table 3 by default) |
| `.poll(seconds)` | re-fetch the content fragment on an interval |
| `.refresh_on(event="dcc:refresh")` | re-fetch when a page event fires. `ChartWidget` and `StatWidget` do this by default, so a table/resource mutation (which fires `dcc:refresh`) repaints them |

## `StatWidget`

`StatWidget.make(label, value=None)` - `.value(x | callable)`, `.description(text)`,
`.icon(name)`, `.query({...})`. A callable value may take `request`.

## `ChartWidget` - Chart.js

`ChartWidget.make(label)`:

- `.kind("line" | "bar" | "area" | "pie" | "doughnut" | "radar")` - `area` is a
  filled line.
- `.data(pairs | {labels, datasets} | callable)` - a `(label, value)` list becomes
  one dataset; a Chart.js `{labels, datasets}` dict passes straight through.
- `.colors([...])` - series colours. Without it a built-in palette
  (`DEFAULT_CHART_PALETTE`, indigo-led) is applied by the renderer: cycled across
  slices for `pie`/`doughnut`/`bar`, one per dataset for `line`/`area`/`radar`. A
  dataset in a hand-built `{labels, datasets}` dict that already carries
  `backgroundColor`/`borderColor` is left untouched.
- `.options(dict)` - merged over `{responsive: true, maintainAspectRatio: false}`.
- `.query({...})` - the no-code data path (below).

Chart.js loads on demand (jsDelivr by default; `DCC["CHARTJS_URL"]` for a
self-hosted copy), only on dashboards that use a chart - the
`DashboardPage` collects each widget's `assets` and emits them once in the page
`<head>`. Nothing is added to `{% dcc_assets %}`.

## `BarListWidget`

`BarListWidget.make(label).data([(label, value), …])` - a dependency-free CSS bar
chart. No JavaScript, no CDN. Good for a compact breakdown where a full charting
library is overkill.

## `TableWidget`

`TableWidget.make(label, table)` - `table` is a `Table` or `table(request)`. The
table keeps its own toolbar, pagination and refresh.

### No-code: `data_source`

In a stored spec there is no `Table` object to pass, so a `data_source` dict
describes one instead:

```json
{"model": "demo.Task",
 "fields": ["title", "priority", "due_on"],
 "filter": {"status": "open"},
 "order_by": ["-due_on"],
 "limit": 50}
```

`resolve_table(spec, request)` turns that into a `Table` with a `TextColumn` per
named field - or every concrete field when `fields` is omitted.

Every key is allowlisted, and validation happens before any query runs:

- `model` must be in `DCC["STUDIO_MODELS"]` (default `[]`, so this is opt-in);
- every entry in `fields`, every `filter` key and every `order_by` term must be
  an allowed path of that model, resolved one relation deep. Sensitive fields
  (`password`, `is_superuser`, `is_staff`, `groups`, `user_permissions`,
  `last_login`) and the auth / sessions / contenttypes models are never allowed;
- `filter` keys may carry one lookup suffix from a fixed set;
- `limit` must be a positive integer and is capped at 200 regardless.

Nothing in the dict comes from a query parameter - it is authored in the studio
and stored. A field a viewer cannot be shown is refused at validation time, not
filtered out afterwards.

## Writing a custom widget

A widget is a Python class + a content template. Override `context(request)` for
plain server-rendered markup, or `payload(request)` to hand a JSON blob to an
Alpine component.

```python
from django_control_components.panels import Widget
from django_control_components.panels.assets import Asset


class SparklineWidget(Widget):
    template_name = "myapp/widgets/sparkline.html"
    variant = "sparkline"  # -> class="dcc-widget--sparkline"
    js_component = "mySparkline"  # Alpine.data() name, optional
    assets = (Asset("script", "https://cdn.jsdelivr.net/npm/…"),)
    auto_refresh = True

    def __init__(self, label, **kwargs):
        super().__init__(**kwargs)
        self._config["label"] = label

    def payload(self, request):
        return {"points": list(self._series(request))}
```

```django
{# myapp/widgets/sparkline.html - the content fragment only, no outer .dcc-widget #}
<div class="dcc-widget__label">{{ label }}</div>
<div x-data="mySparkline('{{ payload_id }}')">
  {{ payload|json_script:payload_id }}
  <svg x-ref="chart"></svg>
</div>
```

The `x-data` must be a single factory call taking the `payload_id` string - no
other `{{ }}` inside `x-data` (a template-linting test enforces this).

## Registering a charting library

`ChartWidget` delegates drawing to a renderer keyed by `payload.library`
(`"chartjs"` is built in). Add another library from your own `<script>`:

```html
<script>
  window.dccWidgets.register("apexcharts", function (node, payload) {
    var chart = new ApexCharts(node, payload.options);
    chart.render();
    return chart;                 // returning something with .destroy() is enough
  });
</script>
```

Then a widget whose `payload()` returns `{"library": "apexcharts", …}` renders
through it. The returned object's `.destroy()` is called before every re-draw and
on teardown, so an htmx fragment swap does not leak the canvas/DOM.

## No-code: `.query({...})`

`ChartWidget.query()` and `StatWidget.query()` take a constrained aggregation spec
resolved server-side - the only chart data path expressible in a stored
`PanelDashboard` JSON row:

```json
{"model": "demo.Task", "group_by": "priority", "aggregate": "count"}
{"model": "demo.Task", "aggregate": "count"}
```

- `model` **must** be listed in `DCC["STUDIO_MODELS"]` - a spec cannot aggregate an
  arbitrary table.
- `aggregate` ∈ `{count, sum, avg, min, max}`; anything but `count` needs
  `aggregate_field`.
- `group_by` / `aggregate_field` are validated against the model's fields.
- `limit` (default 50) caps the number of groups.

A stored dashboard:

```python
PanelDashboard.objects.create(
    slug="metrics",
    label="Metrics",
    widgets=[
        {
            "type": "StatWidget",
            "name": "Tasks",
            "config": {"query": {"model": "demo.Task", "aggregate": "count"}},
        },
        {
            "type": "ChartWidget",
            "name": "By status",
            "config": {
                "kind": "doughnut",
                "query": {"model": "demo.Task", "group_by": "priority", "aggregate": "count"},
            },
        },
    ],
)
```

`Panel(...).dynamic()` serves it at `<panel>/dash/<slug>/` and lists it in the
sidebar. As with resource specs, the client only ever sends the dashboard slug -
never a model label or a type name.
