# Testing

DCC builders render plain HTML through Django's template engine and validate
through Django forms - there is no component runtime to mock. Test them the way
you test any Django view or template fragment.

## Setup

Any test settings that already run Django templates work. The minimum:

```python
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django_cotton",              # must precede django_control_components
    "django_control_components",
    "myapp",
]

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "APP_DIRS": True,
    "OPTIONS": {"builtins": ["django_cotton.templatetags.cotton"]},
}]
```

`APP_DIRS` (or an explicit loader) is required - components call
`render_to_string` on leaf templates shipped in the package. System check
`django_control_components.W002` fires if no Django template backend is
configured.

## Rendering a schema in isolation

`Schema.render(form=...)` returns a `SafeString`. Assert on the markup:

```python
from myapp.schemas import TaskForm, task_schema  # see schemas.md


def test_due_date_is_conditional():
    html = str(task_schema().render(form=TaskForm()))
    # visible_when compiles to an Alpine expression, not a server round-trip
    assert 'x-show' in html
    assert 'name="due_date"' in html


def test_schema_does_not_validate():
    # a schema rendering a subset of a form must not fail on the omitted fields
    html = str(task_schema().render(form=TaskForm(data={"title": "x"})))
    assert "error" not in html.lower() or "This field is required" not in html
```

Labels, choices and `required` come from the bound form - a test that changes the
form field is testing the right thing.

## Rendering a table

`Table.render(request)` takes a request (use `RequestFactory`); it reads
querystring state for sort / filter / search / pagination.

```python
from django.test import RequestFactory
from myapp.tables import task_table


def test_default_sort():
    html = str(task_table().render(RequestFactory().get("/")))
    assert "Ship the release" in html  # a seeded Task


def test_search_narrows_rows():
    req = RequestFactory().get("/", {"_dcc_table": "tasks", "tasks_search": "changelog"})
    html = str(task_table().render(req))
    assert "Ship the release" not in html
```

`.client_side()` forces the in-memory path so a small fixture set behaves
deterministically regardless of `DCC["TABLE_CLIENT_SIDE_MAX_ROWS"]`.

## Testing a `SchemaFormMixin` / `TableMixin` view

Drive these through the test `Client` like any CBV. The extra contract worth a
test is `TableMixin`'s htmx fragment - an `HX-Request` whose `?_dcc_table`
matches the table id returns just the table content, not the full page:

```python
def test_table_fragment(client):
    full = client.get("/tasks/")
    assert b"<html" in full.content

    frag = client.get(
        "/tasks/",
        {"_dcc_table": "tasks"},
        HTTP_HX_REQUEST="true",
    )
    assert b"<html" not in frag.content
    assert b"dcc-table" in frag.content
```

`SchemaFormMixin`: POST valid data, assert the redirect and the saved object;
POST invalid data, assert the re-rendered form carries the field error.

## Testing an action

Actions are POST endpoints mounted by `include("django_control_components.urls")`
at `a/<owner_key>/<action_name>/` (URL name `dcc:action`). GET renders the
confirm / schema modal; POST re-authorizes, re-scopes targets to the owner
queryset, then runs the callback.

```python
from django.urls import reverse


def test_mark_done(client, django_user_model):
    user = django_user_model.objects.create_superuser("s", "s@x.io", "x")
    client.force_login(user)
    url = reverse("dcc:action", args=["table-tasks", "mark_done"])
    resp = client.post(url, {"ids": [t1.pk, t2.pk]})
    assert resp.status_code in (200, 204)
    t1.refresh_from_db()
    assert t1.done is True
```

An unknown owner key or action name is a `404`, never a `500` - worth asserting
if you rely on it.

## Overriding `DCC` settings mid-test

`@override_settings(DCC={...})` takes effect immediately - `dcc_settings` reads
`settings.DCC` on every access, and a `setting_changed` receiver clears the
memoised icon set:

```python
from django.test import override_settings


@override_settings(DCC={"TABLE_CLIENT_SIDE_MAX_ROWS": 1})
def test_flips_to_server_mode():
    html = str(task_table().render(RequestFactory().get("/")))
    assert "hx-get" in html  # server mode wires htmx pagination
```

## Worked examples in this repo

`tests/test_schemas.py`, `tests/test_tables.py`, `tests/test_nav.py`, and the
`tests/testapp/` app are the reference. `tests/conftest.py` has `soup` (a
`BeautifulSoup` parser) and model fixtures.
