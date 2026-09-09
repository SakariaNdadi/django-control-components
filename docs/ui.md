# UI primitives

## Mental model

One Python component + one leaf template per primitive. Every other subsystem
(tables, actions, wizards, panels) composes these instead of hand-writing
`<button>` / `<span class="dcc-badge">` markup - so a restyle or an htmx-version
bump happens in one place. A lint test forbids a hand-rolled `class="dcc-btn"`
anywhere outside this layer.

There are **two** ways to use each primitive:

- **The Python class** (`django_control_components.ui`) - for code that builds HTML
  (a table cell, an action trigger).
- **The `<c-dcc.*>` cotton component** (`templates/cotton/dcc/*.html`) - for
  template authors. These are a *separate, smaller* implementation with a
  `{{ slot }}` and a self-contained trigger where relevant.

```python
from django_control_components.ui import Button, Badge, Icon, Checkbox, Menu, Modal
from django_control_components.core.context import RenderContext

ctx = RenderContext(request=request)
html = Button.make().label("Save").variant("primary").type("submit").render(ctx)
```

Render a Python component in a template with `{% dcc_render component %}`.

## Button (Python)

`Button.make()` → `<button>`, or `<a>` when `.href(...)` is set.

| setter | note |
|---|---|
| `.label(str)` | `None` or `False` both render as empty |
| `.icon(name)` | icon left of the label |
| `.variant(str)` | `primary`, `secondary` (default), `danger`, `ghost`, `link`. **An unknown value warns and falls back to `secondary`.** |
| `.size(str)` | any token → `dcc-btn--<token>` class; only `sm` is styled |
| `.href(url)` | render as `<a>` |
| `.type(str)` | `button` (default), `submit`, `reset` |
| `.disabled()` | |
| `.attributes(bag \| dict)` | merge extra attrs - an htmx `AttributeBag`, Alpine handlers. Repeated calls accumulate. Merged *after* the styling classes so `{{ attrs }}` carries both. |

`IconButton` is a `Button` whose visible content is only the icon; `label`
becomes the `aria-label` and the visible label span is blank. Same setters.

## Badge (Python)

`Badge.make().label("Live").variant("success").icon("circle")` → a pill.

`variant` accepts **any** string → `dcc-badge--<variant>`; the actual set of
styled variants is defined in `css/dcc.css` (`success`, `danger`, `muted`, …) -
an unknown one just yields an unstyled class. `label` is auto-escaped.

## Icon (Python)

`Icon.make("rocket").css_class("text-lg")` renders through the active icon set.
The name is the **positional** argument. Only setter: `.css_class(str)`. Shortcut
tag: `{% dcc_icon "rocket" %}`.

An invalid name (uppercase, dots, slashes, `../`) renders an **empty string
silently** - there is no error for a typo.

## Checkbox (Python)

`Checkbox.make().label("Featured").value("on").checked().attributes({...})` - a
standalone labelled checkbox. `input_name` comes from the component `name`. The
table selection column and the schema `Checkbox` field are separate
implementations.

## Menu (Python)

An Alpine disclosure: a trigger button (default icon `ellipsis-vertical`) and a
list of **pre-rendered HTML item strings**.

```python
Menu.make().icon("ellipsis-vertical").align("end").items(
    [
        edit_action.render_trigger(record=obj, request=request),
        delete_action.render_trigger(record=obj, request=request),
    ]
)
```

| setter | note |
|---|---|
| `.label(str)` | trigger text |
| `.icon(name)` | trigger icon (default `ellipsis-vertical`) |
| `.items([str, …])` | **pre-rendered HTML** - there is no slot |
| `.align("start" \| "end")` | menu alignment (default `end`) |

Opens on click, closes on Escape / click-outside. Used by table row actions
marked `.collapsed()`.

**Why pre-rendered HTML:** a lint test forbids `{{ }}` inside `x-data="{…}"`, so
the Python render path cannot hand a template into the Alpine component - the
items must already be strings.

## Modal (Python)

A teleported overlay with a focus trap (`x-trap.inert.noscroll`). The body is
**pre-rendered HTML** (`.body(...)`) for the same reason as `Menu`.

```python
Modal.make().heading("Confirm").size("sm").body(form_html).render(ctx)
```

| setter | note |
|---|---|
| `.heading(str)` | header text and `aria-label`; header block only renders when set |
| `.size(str)` | any token → `dcc-modal__dialog--<token>` |
| `.body(str \| SafeString)` | rendered with `\|safe` - **the caller owns escaping** |
| `.open_on_load(value=True)` | data flag (default `True`); the action endpoint swaps a ready-open modal into a table's `#dcc-modal-<owner>` mount |
| `.dom_id(str)` | an id for the wrapper |

Close it by swapping the mount empty (what a successful modal action does) or
dispatching the `dcc-modal-close` window event.

The `x-trap` focus containment needs the `@alpinejs/focus` plugin -
`{% dcc_assets %}` emits it before Alpine core. Pass `focus=False` only if the
host page already loads it.

## `<c-dcc.*>` Cotton Components (Frontend Templates)

Template authors can build custom frontend markup using django-cotton components without invoking Python builders. Load with `{% load cotton %}`.

### 1. `<c-dcc.button>`
Renders standard buttons or links with icons and labels:

```django
<c-dcc.button variant="primary" label="Save Changes" type="submit" />
<c-dcc.button href="/articles/new/" icon="plus" label="New Article" />
<c-dcc.button variant="danger" icon="trash">Delete Record</c-dcc.button>
```

- `<c-vars>`: `variant="secondary"` (`primary`, `secondary`, `danger`, `ghost`, `link`), `type="button"`, `href=""` (renders `<a>`), `icon=""` (FontAwesome token), `label=""`, `size=""` (`sm`), `disabled="False"`. Supports `{{ slot }}`.

### 2. `<c-dcc.badge>`
Renders status pills and chips:

```django
<c-dcc.badge label="Published" variant="success" />
<c-dcc.badge variant="danger"><i class="fa-solid fa-triangle-exclamation"></i> Critical</c-dcc.badge>
```

- `<c-vars>`: `label=""`, `variant=""` (`success`, `danger`, `muted`, `secondary`, `primary`). Supports `{{ slot }}`.

### 3. `<c-dcc.heading>`
Renders semantic heading typography:

```django
<c-dcc.heading level="2" title="Account Settings" />
```

- `<c-vars>`: `level="1"` (1 to 6), `title=""`. Supports `{{ slot }}`.

### 4. `<c-dcc.modal>`
Self-contained Alpine.js teleported modal with trigger button and focus trap:

```django
<c-dcc.modal id="confirm-delete" header="Are you sure?" trigger_label="Delete Item" trigger_variant="danger">
  <p class="text-sm text-gray-600">This will permanently delete the project. Are you sure you want to proceed?</p>
  <div class="mt-4 flex justify-end gap-2">
    <button class="dcc-btn dcc-btn--danger">Yes, Delete</button>
  </div>
</c-dcc.modal>
```

- `<c-vars>`: `id="dcc-modal"`, `header=""`, `trigger_label="Open"`, `trigger_variant="primary"`.

### 5. `<c-dcc.form.*>` Form Control Components
Standalone form field wrappers matching DCC styles:

- `<c-dcc.form.input name="email" type="email" label="Email Address" required="True" />`
- `<c-dcc.form.textarea name="bio" label="Bio" rows="4" />`
- `<c-dcc.form.select name="role" label="Role" :options="role_choices" />`
- `<c-dcc.form.checkbox name="agree" label="I agree to terms" />`
- `<c-dcc.form.toggle name="notifications" label="Enable Email Notifications" />`
- `<c-dcc.form.upload name="avatar" label="Profile Picture" />`
- `<c-dcc.form.password name="password" label="Password" />`
- `<c-dcc.form.radio name="tier" :options="tier_choices" />`


## Icon set

```python
DCC = {
    "ICON_SET": "django_control_components.icons.FontAwesome",
    "ICON_ASSET_URL": "https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.7.2/css/all.min.css",
}
```

`ICON_ASSET_URL = None` → the set self-hosts / emits nothing.

### Implementing a set

Satisfy the `IconSet` protocol (`icons/base.py:15-23`):

```python
class MyIcons:
    def __init__(self, asset_url=None):  # optional - see note below
        self.asset_url = asset_url

    def render(self, name, *, css_class=""):  # -> SafeString (already safe)
        ...

    def assets(self):  # -> SafeString of <link>/<script>
        ...
```

- The registry memoises the resolved set with `@lru_cache(maxsize=1)`, keyed on
  `(dotted_path, asset_url)`. It is cleared only when the `DCC` setting itself
  changes (a `setting_changed` receiver - so `override_settings(DCC=...)` in
  tests works).
- The registry calls `cls(asset_url=...)` and, on `TypeError`, retries `cls()` -
  so your set may take the `asset_url` kwarg or not.

### FontAwesome (default)

- Name grammar: `"<style>:<icon>"` or bare `"<icon>"` (default style `solid`).
  Styles: `solid regular light thin duotone brands`. An unrecognised style is
  treated as part of the icon name.
- Icon tokens must match `[a-z0-9-]+`. Anything else → `render()` returns `""`.

## Constraints / do not combine

- `Menu.items(...)` and `Modal.body(...)` are HTML strings, not templates - you
  cannot pass a component; render it first (`component.render(ctx)`).
- `Modal.open_on_load` only sets a data flag; the template's visibility is driven
  by the endpoint that swaps the modal in. For an author-controlled modal use
  `<c-dcc.modal>`.
- `Button.variant()` never raises - it warns and coerces. Watch your dev console.
- `Icon` / `{% dcc_icon %}` never raise on a bad name - they render nothing.

## Known sharp edges

- The two button implementations differ: the Python `Button.variant()` warns and
  coerces; the `<c-dcc.button>` template interpolates `{{ variant }}` verbatim
  into the class (no validation).
- `<c-dcc.modal>` renders its own trigger; the Python `Modal` does not. Do not
  mix the two for one dialog.
