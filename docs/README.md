# Developer Documentation & UI/UX Hub

> **Version `0.0.1`** (Alpha - `0.x` permits breaking changes; see [CHANGELOG](../CHANGELOG.md)).
>
> The core (`schemas`, `tables`, `wizards`, `actions`, `infolists`, `panels`,
> `widgets`, `ui`) is active and tested. **Studio** - the visual builder - ships
> in the optional `[studio]` extra as a **dev-only** prototyping tool
> (`DEBUG=True`; remove it before deploying, per check `dcc_studio.W003`).

Declare UI in Python; it renders through [django-cotton](https://django-cotton.com/), wired directly to real `django.forms` validation without duplicating form state.

---

## ⚡ Tech Stack & Pinned Asset Versions

- **Icons**: **Font Awesome 6.7.2 Free** (solid, regular, light, thin, duotone, brands) via CDN by default (`django_control_components.icons.FontAwesome`), pluggable icon-set protocol.
- **htmx**: **v2.0.4** (`htmx.org@2.0.4`) - powers declarative step swaps, action triggers, keyset stream appends, and table fragments.
- **Alpine.js**: **v3.17.1** (`alpinejs@3.17.1` + `@alpinejs/focus@3.17.1`) - powers reactive dropdowns, modal focus trapping (`x-trap`), and client-side sorting/filtering with zero latency.
- **Templates**: **django-cotton** modern component tags (`<c-dcc.*>`).
- **Forms & Validation**: Standard **`django.forms`** / `ModelForm` - no parallel validation engine.

---

## 🎨 Styling & Overriding CSS

`django-control-components` ships a zero-dependency, theme-aware stylesheet (`dcc.css`). You can customize the look and feel in two ways:

### 1. Overriding CSS Custom Properties (Tokens)

Override variables globally in your project's stylesheet or scope them to specific panels/containers:

```css
:root {
  /* Core brand palette */
  --dcc-primary: #4f46e5;         /* Primary brand color (buttons, active states) */
  --dcc-primary-fg: #ffffff;      /* Contrast text on primary */
  --dcc-radius: 0.5rem;           /* Corner radius for inputs, buttons, cards */
  --dcc-border: #e5e7eb;          /* Border lines */
  --dcc-surface: #f9fafb;         /* Container/card backgrounds */
  
  /* Status alert variants */
  --dcc-success: #16a34a;
  --dcc-danger: #dc2626;
  --dcc-font: Inter, system-ui, sans-serif;
}

/* Dark mode token overrides */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --dcc-bg: #0f172a;
    --dcc-fg: #f8fafc;
    --dcc-primary: #6366f1;
    --dcc-surface: #1e293b;
    --dcc-border: #334155;
  }
}
```

### 2. Custom Tailwind 4 Purging & Theming

If using Tailwind CSS v4, point your build at `css/dcc.css` to tree-shake and purge classes:

```bash
npx @tailwindcss/cli -i css/dcc.css -o static/css/custom-dcc.css
```

---


## 🚀 30-Second Quick Setup

Recommended installation via `uv` (or `pip`):

```bash
# Recommended with uv:
uv add django-control-components
uv add "django-control-components[wizard]"  # + django-formtools for multi-step wizards
uv add "django-control-components[images]"  # + Pillow for image upload & thumbnails

# Or with all optional extras at once:
uv add "django-control-components[wizard,images]"
```

*Using standard pip:*
```bash
pip install "django-control-components[wizard,images]"
```

### Optional Dependencies Matrix

| Extra | Underlying Dependency | When to use |
|---|---|---|
| `[wizard]` | `django-formtools>=2.5` | Multi-step form flows (`WizardView`, `WizardStep`) with htmx step swapping |
| `[images]` | `Pillow>=11` | Image upload validation, aspect-ratio cropping, and thumbnail pipeline |
| `[allauth]` | `django-allauth>=65` | Authentication integration helpers |

### Configure `settings.py`

```python
INSTALLED_APPS = [
    # ...
    "django_cotton",  # must precede django_control_components
    "django_control_components",
]
```

### Add Assets to Base Template

In your base template `<head>` (e.g., `base.html`):

```django
{% load dcc_tags %}
{% dcc_assets %}
```

*(Emits `dcc.css`, the icon-set `<link>` (Font Awesome by default), htmx, `dcc.js`, the Alpine focus plugin, and Alpine.js - in that order. Pass `htmx=False`, `alpine=False`, `focus=False`, or `icons=False` for anything the host page already loads).*

---

## 🛠️ Complete View Implementations

Every snippet below is running in the bundled `web/` project against its `Task`
model (`web/demo/models.py`: `title`, `priority`, `done`, `due_date`). Full
sources in `docs/panels.md`, `docs/tables.md`, `docs/wizards.md`.

### 1. Schema form view (`SchemaFormMixin` + `CreateView`/`UpdateView`)

```python
from django import forms
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django_control_components.mixins import SchemaFormMixin
from django_control_components.schemas import Grid, Schema, Section, Select, TextInput, Toggle
from myapp.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "priority", "done", "due_date"]
        widgets = {"due_date": forms.DateInput(attrs={"type": "date"})}


class TaskCreateView(SchemaFormMixin, CreateView):
    model = Task
    template_name = "tasks/form.html"
    success_url = reverse_lazy("task-list")

    def get_schema(self) -> Schema:
        return (
            Schema.make()
            .form(TaskForm)  # your standard Django ModelForm does the validation
            .schema(
                [
                    Section.make("Task").columns(2).schema(
                        [
                            TextInput.make("title").required().column_span_full(),
                            Select.make("priority"),
                            Toggle.make("done"),
                            TextInput.make("due_date").visible_when("done", equals=False),
                        ]
                    ),
                ]
            )
        )
```

**Template (`tasks/form.html`):**

```django
{% extends "base.html" %}

{% block content %}
<div class="dcc-panel__main">
  <h1>New task</h1>
  <form method="post">
    {% csrf_token %}
    {{ schema_html }}
    <div class="dcc-form__actions">
      <button type="submit" class="dcc-btn dcc-btn--primary">Save</button>
      <a href="{% url 'task-list' %}" class="dcc-btn dcc-btn--secondary">Cancel</a>
    </div>
  </form>
</div>
{% endblock %}
```

### 2. Table view with search, filters and a row action (`TableMixin`)

```python
from django.views.generic import TemplateView
from django_control_components.actions import Action
from django_control_components.tables import (
    BadgeColumn, BooleanColumn, DateColumn, SelectFilter, Table, TableMixin, TextColumn,
)
from myapp.models import Task


def _mark_done(record):
    record.done = True
    record.save(update_fields=["done"])


class TaskListView(TableMixin, TemplateView):
    template_name = "tasks/list.html"

    def get_table(self) -> Table:
        return (
            Table.make(Task.objects.all())
            .id("tasks")
            .columns(
                [
                    TextColumn.make("title").sortable().searchable(),
                    BadgeColumn.make("priority").colors(
                        {"low": "muted", "medium": "secondary", "high": "danger"}
                    ),
                    BooleanColumn.make("done").labels(("✓", "-")),
                    DateColumn.make("due_date").since().sortable(),
                ]
            )
            .filters([SelectFilter.make("priority").options(Task.Priority.choices)])
            .actions([Action.make("mark_done").icon("check").action(_mark_done)])
            .searchable()
            .default_sort("-due_date")
        )
```

**Template (`tasks/list.html`):**

```django
{% extends "base.html" %}
{% load dcc_tags %}

{% block content %}
<div class="dcc-panel__main">
  <header class="dcc-panel__header">
    <h1>Tasks</h1>
    <a href="{% url 'task-create' %}" class="dcc-btn dcc-btn--primary">
      {% dcc_icon "plus" %} New task
    </a>
  </header>
  {{ table_html }}
</div>
{% endblock %}
```

### 3. Multi-step wizard with htmx step swapping (`WizardView`)

```python
from django import forms
from django.shortcuts import redirect
from django_control_components.infolists import BadgeEntry, Infolist, TextEntry
from django_control_components.schemas import Schema, Section, Select, TextInput, Toggle
from django_control_components.wizards import WizardStep, WizardView


class ProjectDetailsForm(forms.Form):
    name = forms.CharField(max_length=100, label="Project name")
    description = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}), required=False)


class ProjectSettingsForm(forms.Form):
    tier = forms.ChoiceField(
        choices=[("starter", "Starter"), ("pro", "Professional"), ("enterprise", "Enterprise")],
        initial="pro",
    )
    is_public = forms.BooleanField(required=False, initial=True)


class ProjectWizard(WizardView):
    show_step_nav = True
    steps_config = [
        WizardStep(
            "details",
            Schema.make().form(ProjectDetailsForm).strict().schema(
                [Section.make("Project").schema(
                    [TextInput.make("name").required(), TextInput.make("description")]
                )]
            ),
            title="Details",
            heading="Project basics",
        ),
        WizardStep(
            "settings",
            Schema.make().form(ProjectSettingsForm).strict().schema(
                [Section.make("Configuration").columns(2).schema(
                    [Select.make("tier").searchable(), Toggle.make("is_public")]
                )]
            ),
            title="Plan & privacy",
        ),
        WizardStep(
            "review",
            Infolist.make().schema(
                [
                    TextEntry.make("name").label("Project name"),
                    BadgeEntry.make("tier").colors(
                        {"starter": "muted", "pro": "primary", "enterprise": "success"}
                    ),
                    TextEntry.make("is_public").label("Public access"),
                ]
            ),
            title="Review",
            heading="Review & confirm",
            record=lambda view: view.get_all_cleaned_data(),
        ),
    ]

    def done(self, form_list, **kwargs):
        data = self.get_all_cleaned_data()
        # ... persist `data` ...
        return redirect("project-list")
```

**Template (`projects/wizard.html`, or use the shipped default):**

```django
{% extends "base.html" %}

{% block content %}
<div class="dcc-panel__main">{{ step_html }}</div>
{% endblock %}
```

---

## 🧭 Subsystems & Complete Customization Matrix

Every component accepts either fluent chaining `.make().foo()` or explicit `kwargs` (`Component(foo=...)`). Developers never need to look into `src/` to find capabilities.

### 📊 Tables Subsystem (`Table`, `*Column`, `*Filter`, `*Action`)
*Full reference: [tables.md](tables.md)*

- **Adaptive Mode Switching**: Automatically toggles between in-memory client-side operations (< 1,000 rows) and keyset-paginated streaming server-side mode (millions of rows with no slow `COUNT(*)`).
- **Column Types & Display**:
  - `TextColumn`: `.limit(n)`, `.badge()`, `.copyable()`, `.align("left"|"center"|"right")`, `.color("emerald"|...)`, `.weight("bold")`
  - `DateColumn`: `.format("Y-m-d")`, `.since()`, `.relative()`
  - `BooleanColumn`: `.labels(("Yes", "No"))`, `.icons(("check", "x"))`
  - `ImageColumn`: `.circular()`, `.stacked()`, `.size(40)`
  - `IconColumn`: Map values to icon names via `.icon(lambda val: ...)`
- **Sorting & Search**:
  - `.sortable(sort_field="db_field")` - safe mapping prevents ORM injection.
  - `.searchable()` / `Table.make().searchable()` - builds multi-column `Q` lookups.
- **Filters**:
  - `SelectFilter`: `.options(...)`, `.multiple()`, `.placeholder(...)`
  - `TernaryFilter`: Boolean / nullable filter with 3-state toggle.
  - `DateRangeFilter`: Filter records within custom start/end timestamps.
  - `QueryFilter`: Custom user-defined ORM query builder.
- **Row & Bulk Actions**:
  - `Action.make(name)`: Single record mutation or navigation. `.modal(schema)`, `.confirm()`, `.to_url(...)`, `.action(callback)`.
  - `BulkAction.make(name)`: Multi-record actions with select-all-matching across whole dataset.
- **Presentation Controls**:
  - `.feed()`: Render as modern feed/card list instead of tabular rows.
  - `.record_url(lambda r: ...)`: Make entire row clickable.
  - `.hover_preview(schema)`: Hover card previewing record details.
  - `.striped()`, `.bordered()`, `.compact()`, `.polling(5000)`.

---

### 🧙 Wizards Subsystem (`WizardView`, `WizardStep`)
*Full reference: [wizards.md](wizards.md)*

- **django-formtools Integration**: Built on `SessionWizardView` for secure multi-step storage, state preservation, and step jumping without boilerplate.
- **htmx Step Swapping**: Seamless step transitions with partial DOM swaps (`#dcc-wizard-step`).
- **Polymorphic Step Bodies**:
  - `Schema` step: Collect and validate form inputs using standard Django `Form` / `ModelForm` classes.
  - `Infolist` step: Read-only summary / confirmation review prior to final submission.
  - `str` / `SafeString` step: Static markdown or raw HTML guidelines/instructions.
  - `callable(view) -> str` step: Dynamic live-calculated markup.
- **Step Configuration & Controls**:
  - `WizardStep("name", body, title="...", heading="...", description="...")`
  - `.skippable(condition=lambda wizard: ...)`
  - `.visible_when(...)`
  - `.allow_goto()`: Enable navigation breadcrumb jumps to completed steps.
  - Custom step validation hooks via `clean_*` or step-specific form definitions.

---

### 🎛️ Panels & Resources Subsystem (`Panel`, `Resource`, `DashboardPage`)
*Full reference: [panels.md](panels.md)*

- **Admin-Independent Architecture**: Complete CRUD surfaces and dashboards without depending on `django.contrib.admin`.
- **Pure Python Declarations**:
  - `Panel(name).path("admin").brand("App", "cubes").resources([...]).pages([...]).auth(...)`
  - Mounts directly into Django URLconf via `panel.mount()`.
- **Resource Lifecycle Methods**:
  - `build_table(request)`: Interactive keyset data table for list view.
  - `build_schema(request)`: Form layout for create and edit pages.
  - `build_infolist(request)`: Read-only summary presentation for detail view.
  - `can(request, action, obj=None)`: Fine-grained permission guards (`view`, `add`, `change`, `delete`).

---

### 📈 Dashboard Widgets Subsystem (`StatWidget`, `ChartWidget`, `BarListWidget`, `TableWidget`)
*Full reference: [widgets.md](widgets.md)*

- **On-Demand Client Libraries**: `Chart.js` is loaded automatically from CDN on-demand only when a `ChartWidget` is present on the page.
- **Widget Types**:
  - `StatWidget`: Key metric cards with `.icon()`, `.description()`, and live background polling via `.poll(seconds)`.
  - `ChartWidget`: Interactive Chart.js charts (`line`, `bar`, `area`, `pie`, `doughnut`, `radar`) with live data refresh on mutations (`dcc:refresh`).
  - `BarListWidget`: Zero-JavaScript CSS bar chart for lightweight distribution views.
  - `TableWidget`: Embedded mini-tables with independent sorting and pagination.
  - Custom Widgets: Subclass `Widget` and supply custom HTML templates / Alpine.js components.


---

### 📑 Complete Reference Directory

| Guide | Description |
|---|---|
| [architecture.md](architecture.md) | Render pipeline, `RenderContext`, `AttributeBag`, fluent/kwargs duality, closure evaluation, invariants |
| [settings.md](settings.md) | Configuration keys `DCC[...]`, asset tagging, system checks, URL registration |
| [schemas.md](schemas.md) | Form layouts (`Section`, `Grid`, `Fieldset`, `Tabs`, reactive `Select`, conditional `visible_when`) |
| [tables.md](tables.md) | Complete table builders, columns, custom filters, pagination, row actions, bulk actions |
| [wizards.md](wizards.md) | Multi-step form flows, step swapping, review steps, formtools bindings |
| [actions.md](actions.md) | Button actions, modal dialogs, bulk operations, authorization hooks |
| [infolists.md](infolists.md) | Read-only record presentation layouts, entries, and badges |
| [ui.md](ui.md) | UI primitives (`Button`, `Badge`, `Icon`, `Checkbox`, `Menu`, `Modal`) & cotton `<c-dcc.*>` tags |
| [panels.md](panels.md) | Admin-independent CRUD resources (`List`, `Create`, `Edit`, `View`, `Delete`) |
| [widgets.md](widgets.md) | Metrics & dashboard widgets (`StatWidget`, `ChartWidget`, `BarListWidget`, `TableWidget`) |
| [images.md](images.md) | Pillow upload pipeline, validation, cropping, thumbnail generation |
| [views-and-mixins.md](views-and-mixins.md) | Class-based view mixins (`SchemaFormMixin`, `TableMixin`, etc.) |
| [callbacks.md](callbacks.md) | Closure injection contracts, evaluation lifecycle |
| [errors.md](errors.md) | System exceptions, error codes, recovery behaviors |
| [no-code.md](no-code.md) | Studio JSON schema definitions *(dev-only, `[studio]` extra)* |
| [deployment.md](deployment.md) | Static files, WhiteNoise, CSP, air-gapped assets, `DEBUG=False` checklist |
| [testing.md](testing.md) | Testing schemas, tables, mixin views, actions; `@override_settings(DCC=...)` |
| [navigation.md](navigation.md) | Sidebar + nav blocks (`NavLink`, collapsible `NavGroup`, `NavUser`), the `dccNav` collapse contract, a11y |
| [../CHANGELOG.md](../CHANGELOG.md) | Release notes; `0.x` breaking-change policy |

