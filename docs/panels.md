# Panels & Resources

A **Panel** is a mount point for a set of **Resources**. A Resource wires one
Django model to four pages - list, create, edit, view - built from the same
`Schema` and `Table` builders you use elsewhere. It is Filament-inspired CRUD
scaffolding on plain class-based views: no Livewire, no server-held component
state, and it touches none of `django.contrib.admin`'s machinery, so the two run
side by side.

Use a panel when you want a branded, permission-gated admin area that you shape
in Python - not a replacement for `django-admin`, and not a place for one-off
pages (yet - see *Custom pages* below).

> **Running example.** Every snippet on this page is the `TaskResource` mounted
> in the `web/` project. Run it (`docs/deployment.md` has the commands) and open
> `/task/` for the live version; the source is `web/demo/pages/full_example.py`
> and `web/demo/panels.py`.

## Define a resource

The demo `Task` model (`web/demo/models.py`) is deliberately small - `title`,
`done`, `priority` (`low` / `medium` / `high`), `due_date`:

```python
# web/demo/pages/full_example.py
from django import forms

from django_control_components.infolists import (
    BadgeEntry, BooleanEntry, DateEntry, Infolist, TextEntry,
)
from django_control_components.panels import Resource
from django_control_components.schemas import (
    FileUpload, Schema, Section, Select, TextInput, Toggle,
)
from django_control_components.tables import (
    BadgeColumn, BooleanColumn, DateColumn, ImageColumn, SelectFilter, Table, TextColumn,
)

from ..models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "priority", "done", "due_date", "cover"]
        widgets = {"due_date": forms.DateInput(attrs={"type": "date"})}


class TaskResource(Resource):
    model = Task
    navigation_icon = "list-check"      # any active-icon-set name
    create_redirect = "list"

    @classmethod
    def can(cls, request, action, obj=None):
        return True                     # this demo is open; drop for Django model perms

    @classmethod
    def build_table(cls, *, request):
        return (
            Table.make(cls.get_queryset(request))
            .id("panel-tasks")
            .columns(
                [
                    ImageColumn.make("cover").thumbnail((32, 32)).rounded(),
                    TextColumn.make("title").sortable().searchable(),
                    BadgeColumn.make("priority").colors(
                        {"low": "muted", "medium": "secondary", "high": "danger"}
                    ),
                    BooleanColumn.make("done").labels(("✓", "-")),
                    DateColumn.make("due_date").since(),
                ]
            )
            .filters([SelectFilter.make("priority").options(Task.Priority.choices)])
            .default_sort("-due_date")
        )

    @classmethod
    def build_schema(cls, *, request):
        return (
            Schema.make()
            .form(TaskForm)
            .schema(
                [
                    Section.make("Task").schema(
                        [
                            TextInput.make("title").required(),
                            Select.make("priority"),
                            Toggle.make("done"),
                            FileUpload.make("cover").image(),
                        ]
                    ),
                    TextInput.make("due_date"),
                ]
            )
        )

    @classmethod
    def build_infolist(cls, *, request):
        return Infolist.make().schema(
            [
                TextEntry.make("title"),
                BadgeEntry.make("priority").colors(
                    {"low": "muted", "medium": "secondary", "high": "danger"}
                ),
                BooleanEntry.make("done"),
                DateEntry.make("due_date"),
            ]
        )
```

Everything is a **classmethod that takes `request`** - never a class attribute -
so per-request state (tenant scoping, the current user) cannot leak between
requests. Override only what you need; the defaults build a five-column table
and a full ModelForm schema.

Override points:

| method | default | use it for |
|---|---|---|
| `build_table(*, request)` | first 5 scalar fields | the list page's `Table` |
| `build_schema(*, request)` | `Schema.make().form(modelform_factory(model))` | the create/edit form |
| `build_infolist(*, request)` | every field as a text entry | the view page (see [infolists.md](infolists.md)) |
| `get_queryset(request)` | `model._default_manager.all()` | row-level / tenant scoping |
| `can(request, action, obj=None)` | Django model perms, superuser bypass | object-level authorization |

`action` is one of `"view"`, `"add"`, `"change"`, `"delete"`.

## Mount the panel

```python
# web/demo/panels.py
from django_control_components.panels import Panel

from .pages.full_example import TaskResource

docs_panel = (
    Panel("docs")
    .path("")                       # mounted at the site root
    .brand("DCC", "cubes")
    .resources([TaskResource])
    .pages([...])                   # non-resource PanelPage classes
)

# web/config/urls.py
urlpatterns = [
    path("dcc/", include("django_control_components.urls")),
    docs_panel.mount(),             # /task/, /task/new/, /task/<pk>/, ...
]
```

Add a guard with `.auth(lambda request: request.user.is_staff)` for a
staff-gated panel; the demo panel is open. `.auth(*guards)` runs before every
page - each guard is `HttpRequest -> bool`, a falsy result raises
`PermissionDenied`. Per-resource `can()` runs after the panel guard.

`.auth(*guards)` runs before every page; each guard is `HttpRequest -> bool` and
a falsy result raises `PermissionDenied`. Add more with repeated `.auth()` calls.
Per-resource `can()` runs after the panel guard.

Routes per resource: `{slug}/`, `{slug}/new/`, `{slug}/<pk>/`, `{slug}/<pk>/edit/`,
`{slug}/<pk>/delete/`. URL names are `{namespace}:{slug}-{list|create|view|edit|delete}`
where the namespace is `dcc-panel-{panel-name}`.

## Skin a panel

The package ships a minimal shell at
`django_control_components/panels/base.html`. Shadow it from your app to drop
panel pages into your own chrome:

```django
{# app/templates/django_control_components/panels/base.html #}
{% extends "app/base.html" %}
{% block crumbs %} / {{ resource_label }}{% endblock %}
```

The list/create/edit/view templates fill `{% block content %}`; context gives you
`panel`, `resource_label`, `nav` (a list of `{label, url, icon, group}`), and -
per page - `table_html`, `schema_html`, or `infolist_html`.

A dashboard page is a grid of widgets - see [widgets.md](widgets.md) for
`StatWidget`, `ChartWidget` (Chart.js), `BarListWidget`, `TableWidget`, custom
widgets, and stored `PanelDashboard` rows.

## Not built yet

- **Relation managers** - inline CRUD of related records on an edit page.
- **Global search** across resources.

See [no-code.md](no-code.md) for building resources from stored configuration
instead of Python subclasses.
