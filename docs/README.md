# Developer Documentation & UI/UX Hub

> **Version `0.0.1`** (Alpha — `0.x` permits breaking changes; see [CHANGELOG](../CHANGELOG.md)).
>
> The core (`schemas`, `tables`, `wizards`, `actions`, `infolists`, `panels`,
> `widgets`, `ui`) is active and tested. **Studio** — the visual builder — ships
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

*(Emits `dcc.css`, the icon-set `<link>` (Font Awesome by default), htmx, `dcc.js`, the Alpine focus plugin, and Alpine.js — in that order. Pass `htmx=False`, `alpine=False`, `focus=False`, or `icons=False` for anything the host page already loads).*

---

## 🛠️ Complete View Implementations

### 1. Full Schema Form View (`SchemaFormMixin` + `CreateView`/`UpdateView`)

```python
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django_control_components.mixins import SchemaFormMixin
from django_control_components.schemas import (
    Grid,
    Schema,
    Section,
    Select,
    TextInput,
    Toggle,
)
from myapp.forms import ArticleForm
from myapp.models import Article


class ArticleCreateView(SchemaFormMixin, CreateView):
    model = Article
    template_name = "articles/form.html"
    success_url = reverse_lazy("article-list")

    def get_schema(self) -> Schema:
        return (
            Schema.make()
            .form(ArticleForm)  # Uses your standard Django ModelForm for validation
            .schema(
                [
                    Section.make("Article Details")
                    .description("Core content and author assignments")
                    .columns(2)
                    .schema(
                        [
                            TextInput.make("title").required().column_span_full(),
                            TextInput.make("slug").required(),
                            Select.make("status").searchable(),
                        ]
                    ),
                    Section.make("Visibility & Schedule").schema(
                        [
                            Toggle.make("is_published"),
                            TextInput.make("published_at").visible_when(
                                "is_published", equals=True
                            ),
                        ]
                    ),
                ]
            )
        )
```

**Template (`articles/form.html`):**
```django
{% extends "base.html" %}

{% block content %}
<div class="max-w-4xl mx-auto py-8">
  <h1 class="text-2xl font-bold mb-6">Create Article</h1>
  <form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ schema_html }}
    <div class="mt-6 flex gap-3">
      <button type="submit" class="dcc-btn dcc-btn--primary">Save Article</button>
      <a href="{% url 'article-list' %}" class="dcc-btn dcc-btn--secondary">Cancel</a>
    </div>
  </form>
</div>
{% endblock %}
```

---

### 2. Full Table View with Search, Keyset Pagination & Bulk Actions (`TableMixin`)

```python
from django.urls import reverse
from django.views.generic import TemplateView
from django_control_components.actions import Action, BulkAction
from django_control_components.tables import (
    BadgeColumn,
    BooleanColumn,
    DateColumn,
    SelectFilter,
    Table,
    TableMixin,
    TextColumn,
)
from myapp.models import Article


class ArticleListView(TableMixin, TemplateView):
    template_name = "articles/list.html"

    def get_table(self) -> Table:
        queryset = Article.objects.select_related("author").all()
        return (
            Table.make(queryset)
            .id("articles-table")
            .columns(
                [
                    TextColumn.make("title")
                    .label("Title")
                    .sortable()
                    .searchable()
                    .limit(64),
                    TextColumn.make("author.username")
                    .label("Author")
                    .sortable(sort_field="author__username"),
                    BadgeColumn.make("status").colors(
                        {"draft": "muted", "review": "secondary", "live": "success"}
                    ),
                    BooleanColumn.make("is_published")
                    .label("Published")
                    .labels(("Live", "Draft")),
                    DateColumn.make("created_at").label("Created").since().sortable(),
                ]
            )
            .filters(
                [
                    SelectFilter.make("status").options(
                        [("draft", "Draft"), ("review", "Review"), ("live", "Live")]
                    ),
                ]
            )
            .actions(
                [
                    Action.make("edit")
                    .icon("pen")
                    .to_url(lambda record: reverse("article-edit", args=[record.pk])),
                ]
            )
            .bulk_actions(
                [
                    BulkAction.make("publish")
                    .icon("check")
                    .requires_confirmation()
                    .action(lambda records: records.update(is_published=True)),
                ]
            )
            .searchable()
            .default_sort("-created_at")
            .record_url(lambda record: reverse("article-edit", args=[record.pk]))
        )
```

**Template (`articles/list.html`):**
```django
{% extends "base.html" %}

{% block content %}
<div class="max-w-7xl mx-auto py-8">
  <div class="flex justify-between items-center mb-6">
    <h1 class="text-2xl font-bold">Articles</h1>
    <a href="{% url 'article-create' %}" class="dcc-btn dcc-btn--primary">New Article</a>
  </div>
  
  {{ table_html }}
</div>
{% endblock %}
```

---

### 3. Full Multi-Step Wizard View with htmx Swapping (`WizardView`)

```python
from django.shortcuts import redirect
from django_control_components.infolists import Infolist, TextEntry
from django_control_components.schemas import Schema, TextInput, Toggle
from django_control_components.wizards import WizardStep, WizardView
from myapp.forms import ArticleDetailsForm, ArticlePublishForm
from myapp.models import Article


class ArticleCreationWizard(WizardView):
    # Optional styling hooks
    wizard_class = "article-wizard-flow"
    show_step_nav = True

    steps_config = [
        # Step 1: Form step for basic details
        WizardStep(
            "details",
            Schema.make()
            .form(ArticleDetailsForm)
            .strict()
            .schema([TextInput.make("title").required(), TextInput.make("slug")]),
            title="Details",
            heading="Article Information",
            description="Enter the main title and URL slug.",
        ),
        # Step 2: Form step for publish settings
        WizardStep(
            "publishing",
            Schema.make()
            .form(ArticlePublishForm)
            .strict()
            .schema([Toggle.make("is_published"), TextInput.make("published_at")]),
            title="Publishing",
            heading="Publication Settings",
        ),
        # Step 3: Review step (Read-only summary using Infolist)
        WizardStep(
            "review",
            Infolist.make().schema(
                [
                    TextEntry.make("title").label("Title"),
                    TextEntry.make("slug").label("URL Slug"),
                    TextEntry.make("is_published").label("Published Immediately?"),
                ]
            ),
            title="Review & Confirm",
            heading="Verify Details",
            description="Please check the information before submitting.",
            record=lambda view: view.get_all_cleaned_data(),
        ),
    ]

    def done(self, form_list, **kwargs):
        # Automatically gathers valid data from all steps
        article_data = self.get_all_cleaned_data()
        article = Article.objects.create(**article_data)
        return redirect("article-detail", pk=article.pk)
```

**Template (`articles/wizard.html` or use the default shipped template):**
```django
{% extends "base.html" %}

{% block content %}
<div class="max-w-3xl mx-auto py-8">
  {{ step_html }}
</div>
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
| [../CHANGELOG.md](../CHANGELOG.md) | Release notes; `0.x` breaking-change policy |

