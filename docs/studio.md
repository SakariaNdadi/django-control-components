# Studio

The studio is the no-code layer: four builders that write JSON specs to the
database, which the panel then renders like any other page. It is a **dev-only
prototyping tool** - a system check (`dcc_studio.W003`) warns when it is
installed with `DEBUG=False`.

[no-code.md](no-code.md) documents the dashboard spec format itself. This page is
about the app around it.

## Install

```bash
pip install "django-control-components[studio]"
```

```python
INSTALLED_APPS = [..., "django_control_components", "django_control_components.studio"]

urlpatterns = [
    path("studio/", include("django_control_components.studio.urls")),
]
```

Then `manage.py migrate`. Access needs `dcc_studio.use_studio` or superuser - see
[permissions.md](permissions.md).

## The builders

| Route | Builds | Stored in |
|---|---|---|
| `/studio/` | index of everything | – |
| `/studio/nav/<panel>/` | the panel sidebar | `NavItem` + `NavDocument` |
| `/studio/dashboards/<slug>/` | a widget dashboard | `DashboardSpec` |
| `/studio/pages/<pk>/` | a standalone page (block tree) | `Page` |
| `/studio/resources/<slug>/` | a CRUD resource over a model | `DashboardSpec` |
| `/studio/roles/` | who can see what | the `AccessControlled` fields |

Each builder has a matching `…/save/` and `…/preview/` endpoint. Preview renders
the unsaved spec server-side, so what you see is the real component tree, not a
mock.

`roles/` is **superuser-only**, separately from `use_studio` - granting someone
the studio does not let them widen their own audience.

## Concurrency

Specs carry a `revision` counter (the nav uses a `NavDocument` row, since a
sidebar is many rows rather than one). A save posts the revision it loaded; if
the stored revision has moved, the server answers **409** with its own copy
instead of overwriting. The builder shows the conflict rather than silently
discarding an edit.

`SpecRevision` keeps the history, so a spec can be rolled back.

## Models

| Model | Holds |
|---|---|
| `DashboardSpec` | a dashboard or resource spec, by slug |
| `StudioEntry` | a `DashboardSpec` proxy for the admin listing |
| `PanelDashboard` | a dashboard mounted into a specific panel |
| `Page` | a standalone page: route, mount point, block tree, `is_home` |
| `NavItem` / `NavDocument` | stored nav rows and their revision token |
| `SpecRevision` | version history for a spec |
| `Notification` | a per-user notification row |
| `UserPreference` | a user's landing page (`home_kind` / `home_target`) |

Everything a viewer can see mixes in `AccessControlled` - `visibility`, `groups`,
`users`, `required_permission`, defaulting to `restricted`.

## What a spec may contain

The deserializer is a sandbox, not a parser. A stored spec:

- names component types from a **registry**, never an import path. An unknown
  name is a validation error; no spec can instantiate an arbitrary class;
- carries **JSON scalars only**, under a 64 KB ceiling and a nesting depth cap;
- cannot set a `CODE_ONLY_SETTERS` key (`action`, `callback`, `authorize`,
  `state`, `visible`, `hidden`, `html`, `extra_attributes`) - these take runtime
  callables or raw HTML;
- cannot set a setter registered `requires="superuser"` (`Column.allow_html`, for
  one) unless the request is from a superuser;
- may only traverse ORM paths that `introspect.safe_paths` allows, which excludes
  sensitive fields (`password`, `is_superuser`, `is_staff`, `groups`,
  `user_permissions`, `last_login`) and the auth / sessions / contenttypes models.

## Escape hatches

Four ways out when the spec cannot express something.

### Custom blocks

Register your own block and it appears in the palette:

```python
from django_control_components.blocks import Block, block

@block("Callout", icon="bullhorn")
class Callout(Block):
    slots = ("default",)
    template_name = "myapp/blocks/callout.html"
```

> If your template renders a value through `|safe`, gate that setter:
> `@block("Embed", setters={"content": {"requires": "superuser"}})`. The
> code-only list knows the setter *names* the library ships - a raw-HTML setter
> under any other name is otherwise writable from a stored spec.

### Callable aliases

A spec may name a project callable, but only through an alias you registered:

```python
DCC = {"STUDIO_CALLABLES": {"is_beta": "myapp.rules.is_beta_tester"}}
```

```json
{"type": "Card", "config": {"visible": "@is_beta"}}
```

Only `visible`, `hidden`, `label` and `url` accept an alias. `authorize` is
deliberately excluded and cannot be added - a stored spec must never name the
callable that decides access. Use the block-level `perms` gate instead.

### Server-side block gating

```json
{"type": "Card", "perms": ["blog.view_article"], "when": "is_beta"}
```

`perms` are ANDed through `has_perm` (superusers pass); `when` names an alias.
Unlike the `visible` / `hidden` props, this gate runs on the server and is
consulted before the block renders.

### Ejecting to Python

When a spec has outgrown the builder, `eject_to_python` prints the equivalent
Python so you can check it into the repo and stop maintaining the spec:

```python
from django_control_components.studio.scaffold import eject_to_python

print(eject_to_python("blog.Article", spec))
```

Going the other way, `manage.py dcc_scaffold` generates a starting spec from a
model, and `scaffold_spec` / `scaffold_dashboard` do the same in code.

## Notifications

A small per-user notification store, plus the `NotificationBell` block.

```python
from django_control_components.studio.notifications import notify

notify(user, "Import finished", level="success", body="412 rows", url="/imports/9/")
```

`notify(user, title, *, level, body, url, actor)` writes a `Notification`;
`unread_count(user)` and `mark_all_read(user)` do what they say.

```python
NotificationBell().interval(15)
```

The bell polls `/studio/notifications/` (its default endpoint) every `interval`
seconds - polling, not websockets. That endpoint is the one studio route open to
**any** authenticated user, and it is scoped to the caller's own rows.

`pending_toasts(request)` drains `django.contrib.messages` into the toast shape,
so an ordinary `messages.success(...)` in any view renders as a toast.

## Data sources

Widgets and stored tables can query a model directly:

```json
{"type": "StatWidget", "config": {"query": {"model": "blog.Article",
  "aggregate": "count", "filter": {"status": "live"}}}}
```

Everything in that dict is allowlisted:

- `model` must be listed in `DCC["STUDIO_MODELS"]`, which defaults to `[]` - so
  the whole feature is opt-in and refuses every model until you name one;
- every field in `fields`, every `filter` key and every `order_by` term must be
  a `safe_paths` entry, with lookups drawn from a fixed set;
- `aggregate` is one of `count`, `sum`, `avg`, `min`, `max`, with the field
  checked for existence;
- `limit` is capped at 200.

Nothing here accepts a query parameter, and there is no raw SQL anywhere in the
library.

## Where to go next

- [no-code.md](no-code.md) - the dashboard spec format
- [blocks.md](blocks.md) - the block tree the page builder edits
- [permissions.md](permissions.md) - `use_studio`, visibility, the roles screen
- [navigation.md](navigation.md) - the stored-nav half of the sidebar
- [widgets.md](widgets.md) - the widgets a dashboard spec can place
