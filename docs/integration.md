# Integrating into an existing project

Most docs here show a greenfield setup where a `Panel` owns the whole page. If
your project already has its own `base.html`, navigation and styling, you do not
have to adopt any of that. Pick the level you want.

| Level | You keep | You get |
|---|---|---|
| 1. Render a block | your templates, your layout | one component, anywhere |
| 2. Rendered HTML strings | your templates, your views | tables / forms / infolists in your own pages |
| 3. `AppShell` | your `<html>`, your assets | the panel chrome (drawer, theme toggle) without a `Panel` |
| 4. Shadow the panel base | the panel routing | your own skin over the whole panel |

All four need the same two pieces of setup.

## Setup

`{% dcc_assets %}` in your `<head>`, once:

```django
{% load dcc_tags %}
<head>
  {% dcc_assets %}
</head>
```

It emits, in this order: `dcc.css`, the icon stylesheet, htmx, `dcc.js`, the
Alpine focus plugin, then Alpine core. **The order is load-bearing** - `dcc.js`
must precede Alpine so its `alpine:init` listener is registered first. Do not
reorder them, and do not load your own Alpine separately.

The keyword arguments turn off pieces you already have:
`{% dcc_assets htmx=False %}`, likewise `alpine=`, `icons=`, `focus=`.

And the internal endpoints, for htmx actions and live field validation:

```python
urlpatterns = [
    path("dcc/", include("django_control_components.urls")),
]
```

## Level 1: render any block into any template

`{% dcc_render %}` takes any constructed `Component` or `Block` and renders it in
place. No panel, no resource, no registration.

```python
from django_control_components.blocks import Card, Prose

def dashboard(request):
    card = (
        Card()
        .fill("header", [Prose().html("<h2>Today</h2>")])
        .fill("body", widgets)
    )
    return render(request, "myapp/dashboard.html", {"card": card})
```

```django
{% extends "myapp/base.html" %}
{% load dcc_tags %}
{% block content %}
  {% dcc_render card %}
{% endblock %}
```

The tag builds a `RenderContext` from the template context's `request` and `form`,
so blocks that depend on either work without extra plumbing.

Your own blocks work identically - subclass `Block`, point it at a template, and
optionally register it so the studio can offer it. See [blocks.md](blocks.md).

## Level 2: rendered HTML strings

`Table`, `Schema`, `Infolist` and wizards render themselves rather than going
through `Component`, so they arrive in your context as HTML strings. The mixins
put them there:

```python
from django_control_components.mixins import SchemaFormMixin

class ArticleCreate(SchemaFormMixin, CreateView):
    model = Article
    schema = article_schema
    template_name = "myapp/article_form.html"
```

```django
{% extends "myapp/base.html" %}
{% block content %}
  {{ schema_html }}
{% endblock %}
```

`SchemaFormMixin` sets `schema` and `schema_html`. `TableMixin` (from
`django_control_components.tables`) sets `table_html` - renamable via
`table_context_name` - and additionally serves the htmx fragment on a matching
`?_dcc_table` request, which is what makes sorting and pagination work without a
full page load. Full details in [views-and-mixins.md](views-and-mixins.md).

You can also skip the mixins entirely and render into your own context:

```python
context["table_html"] = my_table.render(request)
```

Doing that gives up the fragment contract, so the table falls back to full-page
reloads. Use `TableMixin` unless you have a reason not to.

## Level 3: `AppShell` - panel chrome without a panel

`AppShell` is the block equivalent of the panel shell. It emits the same
`.dcc-panel` root and `dccShell()` scope, so the responsive drawer, the nav
toggle, the scrim and `ThemeToggle` all work - inside your own document.

```python
shell = (
    AppShell()
    .fill("sidebar", [my_sidebar])
    .fill("content", [page_body])
)
```

```django
{% extends "myapp/base.html" %}
{% load dcc_tags %}
{% block body %}{% dcc_render shell %}{% endblock %}
```

Slots: `topbar`, `sidebar`, `content`, `footer`. All optional - when there is no
topbar and no footer, `<main>` becomes a direct child of the root, matching
`panels/base.html` exactly. `.sidebar_width("18rem")` sets the drawer width
(default `15rem`).

> `AppShell` renders a `<div>`, not a document. It does **not** emit
> `{% dcc_assets %}` - your page still has to, and `ThemeToggle` needs the
> `dccShell()` scope that `AppShell` provides, so keep the toggle inside it.

### Building a sidebar without a panel

If you are not using `Panel`, build the `Sidebar` block directly:

```python
sidebar = (
    Sidebar()
    .brand("Acme").brand_icon("bolt").brand_url("/")
    .fill("default", [
        NavHeading().label("Content"),
        NavLink().label("Articles").icon("file").to("article-list"),
        NavGroup().label("Settings").open().fill("default", [
            NavLink().label("Team").to("team"),
        ]),
    ])
    .fill("footer", [ThemeToggle()])
)
```

`.to()` takes a path, an `#anchor`, or a URL name (reversed; a miss renders `#`).
If you *do* have a panel and only want its tree rendered somewhere else, use
`sidebar_from_tree` - see [navigation.md](navigation.md).

## Level 4: shadow the panel base

If you want the panel's routing and pages but your own chrome, shadow its
template. Create `django_control_components/panels/base.html` in a template
directory that precedes the package's, and extend your own base:

```django
{# myapp/templates/django_control_components/panels/base.html #}
{% extends "myapp/base.html" %}
{% load dcc_tags %}

{% block head_extra %}
  <link rel="stylesheet" href="{% static 'myapp/panel.css' %}">
  {% for asset in widget_assets %}
    {% if asset.kind == "style" %}<link rel="stylesheet" href="{{ asset.url }}">
    {% else %}<script defer src="{{ asset.url }}"></script>{% endif %}
  {% endfor %}
{% endblock %}

{% block content %}
  {% dcc_render sidebar %}
  {{ block.super }}
{% endblock %}
```

Keep `{% dcc_render sidebar %}` (or the `panels/_nav.html` partial, which wraps
the same call in an `{% if sidebar %}`) or the nav disappears.

Context every panel page provides: `panel`, `resource_label`, `sidebar` (a
`Sidebar` block instance, not HTML), `nav_tree` (`NavNode`s), `nav` (the same as
flat dicts), `content_style`, and per page one of `table_html` / `schema_html` /
`infolist_html` / `widgets` / `widget_assets`.

`widget_assets` matters: widgets declare their own scripts (Chart.js, for one)
and nothing loads them unless your shadowed base emits them, as above.

## Styling

`dcc.css` is theme-aware and driven by custom properties, so the usual move is to
override tokens rather than write rules:

```css
:root { --dcc-primary: #6d28d9; --dcc-radius: 4px; }
.dcc-panel { --dcc-panel-nav-w: 18rem; }
```

The core tokens are `--dcc-bg`, `--dcc-surface`, `--dcc-fg`, `--dcc-muted`,
`--dcc-border`, `--dcc-primary` / `--dcc-primary-fg`, `--dcc-danger` /
`--dcc-danger-fg`, `--dcc-success`, `--dcc-warning`, `--dcc-focus`,
`--dcc-radius`, `--dcc-gap` and `--dcc-font`. Each is defined for both themes,
so overriding one on `:root` follows light and dark automatically. See
[docs/README.md](README.md) for the full list and the theming contract.

## Where to go next

- [blocks.md](blocks.md) - the block tree and writing your own
- [views-and-mixins.md](views-and-mixins.md) - every mixin and its context keys
- [navigation.md](navigation.md) - nav blocks and the panel sidebar
- [permissions.md](permissions.md) - what a panel guard does and does not cover
- [deployment.md](deployment.md) - self-hosted assets, CSP, `DEBUG=False`
