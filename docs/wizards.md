# Wizards

## Mental model

Multi-step forms on top of `django-formtools`. `formtools` already solves step
storage, inter-step file handling, step re-entry and `done()`. `WizardView`
subclasses its `SessionWizardView` and **swaps only the rendering layer**.

Per-step validation is Django's `form.is_valid()` - there is no parallel system.
A form step's form contains **only that step's declared fields**
(`schema.to_form_class()`).

```bash
pip install "django-control-components[wizard]"
```

Calling `WizardView.as_view()` without `django-formtools` installed raises
`RuntimeError("WizardView needs django-formtools. Install
django-control-components[wizard].")`.

## Quick start

This is the live wizard from the `web/` project - `/wizards/`, source
`web/demo/pages/wizard_demo.py`:

```python
from django import forms
from django.shortcuts import redirect

from django_control_components.infolists import BadgeEntry, Infolist, TextEntry
from django_control_components.schemas import Schema, Section, Select, TextInput, Toggle
from django_control_components.wizards import WizardStep, WizardView


class ProjectDetailsForm(forms.Form):
    name = forms.CharField(max_length=100, label="Project Name")
    description = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}), required=False)


class ProjectSettingsForm(forms.Form):
    tier = forms.ChoiceField(
        choices=[("starter", "Starter"), ("pro", "Professional"), ("enterprise", "Enterprise")],
        initial="pro",
    )
    is_public = forms.BooleanField(required=False, initial=True, label="Publicly discoverable")


class ProjectWizard(WizardView):
    show_step_nav = True
    steps_config = [
        WizardStep(
            "details",
            Schema.make().form(ProjectDetailsForm).strict().schema(
                [
                    Section.make("Project information").schema(
                        [TextInput.make("name").required(), TextInput.make("description")]
                    ),
                ]
            ),
            title="Details",
            heading="Project basics",
        ),
        WizardStep(
            "settings",
            Schema.make().form(ProjectSettingsForm).strict().schema(
                [
                    Section.make("Configuration").columns(2).schema(
                        [Select.make("tier").searchable(), Toggle.make("is_public")]
                    ),
                ]
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

## `WizardStep`

```python
WizardStep(name, body, *, title="", heading="", description="", record=None)
```

| field | meaning |
|---|---|
| `name` | step id (used in `form_list`, `steps_config` lookups, goto buttons) |
| `body` | polymorphic - see below |
| `title` | step-nav label (default: `name.title()`) |
| `heading` / `description` | strings rendered above the body (`""` when unset) |
| `record` | `callable(view) -> record` for an `Infolist` body; a `dict` return is wrapped in `SimpleNamespace` |

### `body` types

| `body` | step is | use for |
|---|---|---|
| `Schema` | a form step | collect + validate fields (Django's `is_valid()`) |
| `Infolist` | a read-only step | review collected data, show a record |
| `str` / `SafeString` | raw markup | intro screen, static instructions |
| `callable(view) -> str` | rendered markup | "what changed" notes needing live data |

Non-form bodies get an empty, always-valid form - **`Next` never blocks** on them
and they contribute nothing to `form_list` / `get_all_cleaned_data()`.

```python
from django_control_components.infolists import Infolist, TextEntry

steps_config = [
    WizardStep(
        "intro",
        "<p>Nothing is saved until the final step.<p>",
        title="Start",
        heading="Before you begin",
    ),
    WizardStep("details", project_details_schema(), title="Details"),
    WizardStep(
        "review",
        Infolist.make().schema([TextEntry.make("name"), TextEntry.make("tier")]),
        title="Review",
        heading="Confirm",
        record=lambda view: view.get_all_cleaned_data(),
    ),
]
```

## `WizardView`

### Class attributes

| attribute | default | meaning |
|---|---|---|
| `steps_config` | `[]` | **required** - the list of `WizardStep` |
| `template_name` | a shipped template | override for full structural control |
| `wizard_class` | `""` | extra class on `.dcc-wizard` |
| `wizard_attrs` | `{}` | attributes on the wrapper - a `style` string setting `--dcc-wizard-*` custom properties is the intended path |
| `show_step_nav` | `True` | set `False` to drop the step `<ol>` |

### `__init_subclass__` derives `form_list`

When you set `steps_config` **as a class attribute**, `__init_subclass__` builds
`form_list = [(name, form_class) for each step]` and, if you did not set
`file_storage`, points it at `MEDIA_ROOT/dcc-wizard-tmp`.

**Do not set `form_list` yourself** - it is derived. Do not build `steps_config`
in `__init__` - the class-attribute hook won't see it.

### Methods

| method | override? | note |
|---|---|---|
| `done(form_list, **kwargs)` | **required** | the base raises `NotImplementedError`. Persist the data, return a response. |
| `get_context_data(form, **kwargs)` | rarely | adds the template context (below); calls `super()` |
| `render_done(form, **kwargs)` | no | re-validates **every** prior step before `done()`; promotes an htmx 3xx to a real browser redirect |

`render_done` guarantee: a hand-crafted POST cannot skip ahead - every prior
step's stored data is re-run through `form.is_valid()` first
(`wizards/wizard.py:198-221`).

## Theming

Chrome is themed per subclass, no template override:

```python
class ProjectWizard(WizardView):
    wizard_class = "project-wizard"
    wizard_attrs = {
        "style": "--dcc-wizard-bg:#0b1120;--dcc-wizard-pad:2rem;"
        "--dcc-wizard-accent:#6366f1;--dcc-wizard-accent-fg:#fff",
    }
    show_step_nav = True
```

| Custom property | Default | Effect |
|---|---|---|
| `--dcc-wizard-bg` | `transparent` | wrapper background |
| `--dcc-wizard-accent` | `var(--dcc-primary)` | current-step chip background |
| `--dcc-wizard-accent-fg` | `var(--dcc-primary-fg)` | current-step chip text |
| `--dcc-wizard-pad` | `0` | wrapper padding |
| `--dcc-wizard-radius` | `var(--dcc-radius)` | wrapper corner radius |

## Template contract

The shipped template renders (context provided by `get_context_data`):

| var | meaning |
|---|---|
| `step_html` | rendered body of the current step (`schema_html` is a back-compat alias) |
| `step_heading` / `step_description` | per-step strings, `""` when unset |
| `steps` | `[{name, title, is_current, is_done, can_goto}]` |
| `step_titles` | `[(name, title)]` - back-compat alias |
| `current_step` | current step name |
| `all_data` | `get_all_cleaned_data()`, or `{}` if a prior step is invalid |
| `wizard_id` | `dcc-wizard-<classname-lower>` |
| `wizard_htmx` | the htmx attribute bag for the step form (POST + `hx-select` of the wizard node) |
| `wizard_class`, `wizard_attrs_html`, `show_step_nav` | theming hooks |

Each step submits over htmx and swaps only `#<wizard_id>` back in - the view
still renders the full page, so **with JavaScript disabled the plain full-page
POST flow is unchanged**. The step `<ol>` sits outside the `<form>` (its goto
buttons target it by `form="..."`) so pressing Enter in a field always submits
`Next`, never a jump back.

Prior steps carry `can_goto=True`; forward navigation stays `formtools`
validation-gated (you cannot skip ahead).

## Constraints / do not combine

- Set `steps_config` as a class attribute, not in `__init__`.
- Do not set `form_list` - it is derived from `steps_config`.
- `done()` must be implemented - the base raises `NotImplementedError`.
- A `Schema` step should use `.strict()` so its standalone form binds only the
  step's fields; without it, unmapped fields of the parent form are appended.
- An `Infolist` step needs `record=` (a callable) or it renders against `None`.

## Known sharp edges

- `_all_data()` swallows any exception from `get_all_cleaned_data()` and returns
  `{}` - a review step rendered before a prior step is valid shows nothing, not
  an error.
- `WizardStep.record` is called on every render of that step; keep it cheap.
- The default `file_storage` is a `FileSystemStorage` under `MEDIA_ROOT`; set
  `file_storage` explicitly for S3 / remote media.
