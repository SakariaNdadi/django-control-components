# DCC Components Configuration Reference
A complete list of all components and their `@setter` configuration options.

## Infolist Entries

### `BadgeEntry`
**Label:** Badge
**Category:** entry

| Setter | Type | Default | Description |
|---|---|---|---|
| `.colors()` | `keyvalue` | **required** |  |
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.label()` | `string` | **required** |  |
| `.placeholder()` | `string` | **required** |  |
| `.state()` | `object` | **required** |  |
| `.visible()` | `unknown` | **required** |  |

### `BooleanEntry`
**Label:** Boolean
**Category:** entry

| Setter | Type | Default | Description |
|---|---|---|---|
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.label()` | `string` | **required** |  |
| `.placeholder()` | `string` | **required** |  |
| `.state()` | `object` | **required** |  |
| `.visible()` | `unknown` | **required** |  |

### `DateEntry`
**Label:** Date
**Category:** entry

| Setter | Type | Default | Description |
|---|---|---|---|
| `.date_format()` | `string` | **required** |  |
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.label()` | `string` | **required** |  |
| `.placeholder()` | `string` | **required** |  |
| `.since()` | `boolean` | `True` |  |
| `.state()` | `object` | **required** |  |
| `.visible()` | `unknown` | **required** |  |

### `TextEntry`
**Label:** Text
**Category:** entry

| Setter | Type | Default | Description |
|---|---|---|---|
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.label()` | `string` | **required** |  |
| `.placeholder()` | `string` | **required** |  |
| `.state()` | `object` | **required** |  |
| `.visible()` | `unknown` | **required** |  |

## Schema Fields

### `Checkbox`
**Category:** field

| Setter | Type | Default | Description |
|---|---|---|---|
| `.column_span()` | `string` | **required** |  |
| `.default()` | `object` | **required** |  |
| `.disabled()` | `boolean` | `True` |  |
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.help_text()` | `string` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.hint()` | `string` | **required** |  |
| `.icon()` | `string` | **required** |  |
| `.label()` | `string` | **required** |  |
| `.live()` | `string` | `True` |  |
| `.placeholder()` | `string` | **required** |  |
| `.readonly()` | `boolean` | `True` |  |
| `.required()` | `boolean` | `True` |  |
| `.visible()` | `unknown` | **required** |  |

### `EmailInput`
**Label:** Email
**Category:** field

| Setter | Type | Default | Description |
|---|---|---|---|
| `.column_span()` | `string` | **required** |  |
| `.default()` | `object` | **required** |  |
| `.disabled()` | `boolean` | `True` |  |
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.help_text()` | `string` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.hint()` | `string` | **required** |  |
| `.icon()` | `string` | **required** |  |
| `.label()` | `string` | **required** |  |
| `.live()` | `string` | `True` |  |
| `.placeholder()` | `string` | **required** |  |
| `.readonly()` | `boolean` | `True` |  |
| `.required()` | `boolean` | `True` |  |
| `.visible()` | `unknown` | **required** |  |

### `Fieldset`
**Category:** layout

| Setter | Type | Default | Description |
|---|---|---|---|
| `.columns()` | `number` | **required** |  |
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.visible()` | `unknown` | **required** |  |

### `FileUpload`
**Label:** File upload
**Category:** field

| Setter | Type | Default | Description |
|---|---|---|---|
| `.accept()` | `string` | **required** |  |
| `.allow_svg()` | `boolean` | `True` |  |
| `.aspect_ratio()` | `string` | **required** |  |
| `.aspect_tolerance()` | `number` | **required** | Allowed deviation from ``aspect_ratio``, as a fraction (default 0.02 = ±2%). |
| `.column_span()` | `string` | **required** |  |
| `.convert()` | `string` | **required** |  |
| `.default()` | `object` | **required** |  |
| `.disabled()` | `boolean` | `True` |  |
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.help_text()` | `string` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.hint()` | `string` | **required** |  |
| `.icon()` | `string` | **required** |  |
| `.image()` | `boolean` | `True` |  |
| `.label()` | `string` | **required** |  |
| `.live()` | `string` | `True` |  |
| `.max_dimensions()` | `number` | **required** |  |
| `.max_size()` | `string` | **required** |  |
| `.min_dimensions()` | `number` | **required** |  |
| `.placeholder()` | `string` | **required** |  |
| `.readonly()` | `boolean` | `True` |  |
| `.required()` | `boolean` | `True` |  |
| `.resize()` | `number` |  |  |
| `.strip_exif()` | `boolean` | `True` |  |
| `.visible()` | `unknown` | **required** |  |

### `Grid`
**Category:** layout

| Setter | Type | Default | Description |
|---|---|---|---|
| `.columns()` | `number` | **required** |  |
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.visible()` | `unknown` | **required** |  |

### `Hidden`
**Category:** field

| Setter | Type | Default | Description |
|---|---|---|---|
| `.column_span()` | `string` | **required** |  |
| `.default()` | `object` | **required** |  |
| `.disabled()` | `boolean` | `True` |  |
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.help_text()` | `string` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.hint()` | `string` | **required** |  |
| `.icon()` | `string` | **required** |  |
| `.label()` | `string` | **required** |  |
| `.live()` | `string` | `True` |  |
| `.placeholder()` | `string` | **required** |  |
| `.readonly()` | `boolean` | `True` |  |
| `.required()` | `boolean` | `True` |  |
| `.visible()` | `unknown` | **required** |  |

### `MultiSelect`
**Label:** Multi-select
**Category:** field

| Setter | Type | Default | Description |
|---|---|---|---|
| `.column_span()` | `string` | **required** |  |
| `.default()` | `object` | **required** |  |
| `.disabled()` | `boolean` | `True` |  |
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.help_text()` | `string` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.hint()` | `string` | **required** |  |
| `.icon()` | `string` | **required** |  |
| `.label()` | `string` | **required** |  |
| `.live()` | `string` | `True` |  |
| `.options()` | `object` | **required** |  |
| `.placeholder()` | `string` | **required** |  |
| `.readonly()` | `boolean` | `True` |  |
| `.required()` | `boolean` | `True` |  |
| `.searchable()` | `boolean` | `True` |  |
| `.visible()` | `unknown` | **required** |  |

### `PasswordInput`
**Label:** Password
**Category:** field

| Setter | Type | Default | Description |
|---|---|---|---|
| `.column_span()` | `string` | **required** |  |
| `.default()` | `object` | **required** |  |
| `.disabled()` | `boolean` | `True` |  |
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.help_text()` | `string` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.hint()` | `string` | **required** |  |
| `.icon()` | `string` | **required** |  |
| `.label()` | `string` | **required** |  |
| `.live()` | `string` | `True` |  |
| `.placeholder()` | `string` | **required** |  |
| `.readonly()` | `boolean` | `True` |  |
| `.required()` | `boolean` | `True` |  |
| `.visible()` | `unknown` | **required** |  |

### `Radio`
**Label:** Radio group
**Category:** field

| Setter | Type | Default | Description |
|---|---|---|---|
| `.column_span()` | `string` | **required** |  |
| `.default()` | `object` | **required** |  |
| `.disabled()` | `boolean` | `True` |  |
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.help_text()` | `string` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.hint()` | `string` | **required** |  |
| `.icon()` | `string` | **required** |  |
| `.label()` | `string` | **required** |  |
| `.live()` | `string` | `True` |  |
| `.options()` | `object` | **required** |  |
| `.placeholder()` | `string` | **required** |  |
| `.readonly()` | `boolean` | `True` |  |
| `.required()` | `boolean` | `True` |  |
| `.searchable()` | `boolean` | `True` |  |
| `.visible()` | `unknown` | **required** |  |

### `Section`
**Category:** layout

| Setter | Type | Default | Description |
|---|---|---|---|
| `.columns()` | `number` | **required** |  |
| `.description()` | `string` | **required** |  |
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.visible()` | `unknown` | **required** |  |

### `Select`
**Category:** field

| Setter | Type | Default | Description |
|---|---|---|---|
| `.column_span()` | `string` | **required** |  |
| `.default()` | `object` | **required** |  |
| `.disabled()` | `boolean` | `True` |  |
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.help_text()` | `string` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.hint()` | `string` | **required** |  |
| `.icon()` | `string` | **required** |  |
| `.label()` | `string` | **required** |  |
| `.live()` | `string` | `True` |  |
| `.options()` | `object` | **required** |  |
| `.placeholder()` | `string` | **required** |  |
| `.readonly()` | `boolean` | `True` |  |
| `.required()` | `boolean` | `True` |  |
| `.searchable()` | `boolean` | `True` |  |
| `.visible()` | `unknown` | **required** |  |

### `Tab`
**Category:** layout

| Setter | Type | Default | Description |
|---|---|---|---|
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.visible()` | `unknown` | **required** |  |

### `Tabs`
**Category:** layout

| Setter | Type | Default | Description |
|---|---|---|---|
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.visible()` | `unknown` | **required** |  |

### `TextInput`
**Label:** Text
**Category:** field

| Setter | Type | Default | Description |
|---|---|---|---|
| `.column_span()` | `string` | **required** |  |
| `.default()` | `object` | **required** |  |
| `.disabled()` | `boolean` | `True` |  |
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.help_text()` | `string` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.hint()` | `string` | **required** |  |
| `.icon()` | `string` | **required** |  |
| `.label()` | `string` | **required** |  |
| `.live()` | `string` | `True` |  |
| `.placeholder()` | `string` | **required** |  |
| `.readonly()` | `boolean` | `True` |  |
| `.required()` | `boolean` | `True` |  |
| `.visible()` | `unknown` | **required** |  |

### `Textarea`
**Label:** Text area
**Category:** field

| Setter | Type | Default | Description |
|---|---|---|---|
| `.column_span()` | `string` | **required** |  |
| `.default()` | `object` | **required** |  |
| `.disabled()` | `boolean` | `True` |  |
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.help_text()` | `string` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.hint()` | `string` | **required** |  |
| `.icon()` | `string` | **required** |  |
| `.label()` | `string` | **required** |  |
| `.live()` | `string` | `True` |  |
| `.placeholder()` | `string` | **required** |  |
| `.readonly()` | `boolean` | `True` |  |
| `.required()` | `boolean` | `True` |  |
| `.visible()` | `unknown` | **required** |  |

### `Toggle`
**Category:** field

| Setter | Type | Default | Description |
|---|---|---|---|
| `.column_span()` | `string` | **required** |  |
| `.default()` | `object` | **required** |  |
| `.disabled()` | `boolean` | `True` |  |
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.help_text()` | `string` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.hint()` | `string` | **required** |  |
| `.icon()` | `string` | **required** |  |
| `.label()` | `string` | **required** |  |
| `.live()` | `string` | `True` |  |
| `.placeholder()` | `string` | **required** |  |
| `.readonly()` | `boolean` | `True` |  |
| `.required()` | `boolean` | `True` |  |
| `.visible()` | `unknown` | **required** |  |

## Dashboard Widgets

### `BarListWidget`
**Label:** Bar list
**Category:** widget
> A dependency-free CSS bar chart - ``.data([(label, value), ...])``.

| Setter | Type | Default | Description |
|---|---|---|---|
| `.columns()` | `number` | **required** |  |
| `.data()` | `object` | **required** |  |
| `.id()` | `string` | **required** |  |
| `.poll()` | `number` | **required** |  |
| `.refresh_on()` | `string` | `dcc:refresh` |  |

### `ChartWidget`
**Label:** Chart
**Category:** widget
> A Chart.js chart. ``.data([(label, value), ...])`` or a ``{labels, datasets}``

| Setter | Type | Default | Description |
|---|---|---|---|
| `.colors()` | `list` | **required** | Series colours for this chart. Overrides :data:`DEFAULT_CHART_PALETTE`. |
| `.columns()` | `number` | **required** |  |
| `.data()` | `object` | **required** |  |
| `.id()` | `string` | **required** |  |
| `.kind()` | `string` | **required** |  |
| `.options()` | `keyvalue` | **required** |  |
| `.poll()` | `number` | **required** |  |
| `.query()` | `keyvalue` | **required** |  |
| `.refresh_on()` | `string` | `dcc:refresh` |  |

### `StatWidget`
**Label:** Stat
**Category:** widget

| Setter | Type | Default | Description |
|---|---|---|---|
| `.columns()` | `number` | **required** |  |
| `.description()` | `string` | **required** |  |
| `.icon()` | `string` | **required** |  |
| `.id()` | `string` | **required** |  |
| `.poll()` | `number` | **required** |  |
| `.query()` | `keyvalue` | **required** |  |
| `.refresh_on()` | `string` | `dcc:refresh` |  |
| `.value()` | `object` | **required** |  |

### `TableWidget`
**Label:** Table
**Category:** widget

| Setter | Type | Default | Description |
|---|---|---|---|
| `.columns()` | `number` | **required** |  |
| `.data_source()` | `object` | **required** | A stored ``DataSource`` dict (``{model, fields, filter, order_by, |
| `.id()` | `string` | **required** |  |
| `.poll()` | `number` | **required** |  |
| `.refresh_on()` | `string` | `dcc:refresh` |  |
| `.table()` | `object` | **required** |  |

## Table Columns

### `BadgeColumn`
**Label:** Badge
**Category:** column

| Setter | Type | Default | Description |
|---|---|---|---|
| `.align()` | `string` | **required** |  |
| `.allow_html()` | `boolean` | `True` |  |
| `.colors()` | `keyvalue` | **required** |  |
| `.label()` | `string` | **required** |  |
| `.limit()` | `number` | **required** |  |
| `.searchable()` | `string` | `True` |  |
| `.sortable()` | `string` | `True` |  |
| `.state()` | `object` | **required** | Override the displayed value: ``lambda record: ...``. |

### `BooleanColumn`
**Label:** Boolean
**Category:** column

| Setter | Type | Default | Description |
|---|---|---|---|
| `.align()` | `string` | **required** |  |
| `.allow_html()` | `boolean` | `True` |  |
| `.label()` | `string` | **required** |  |
| `.labels()` | `list` | **required** |  |
| `.limit()` | `number` | **required** |  |
| `.searchable()` | `string` | `True` |  |
| `.sortable()` | `string` | `True` |  |
| `.state()` | `object` | **required** | Override the displayed value: ``lambda record: ...``. |

### `DateColumn`
**Label:** Date
**Category:** column

| Setter | Type | Default | Description |
|---|---|---|---|
| `.align()` | `string` | **required** |  |
| `.allow_html()` | `boolean` | `True` |  |
| `.date_format()` | `string` | **required** |  |
| `.label()` | `string` | **required** |  |
| `.limit()` | `number` | **required** |  |
| `.searchable()` | `string` | `True` |  |
| `.since()` | `boolean` | `True` |  |
| `.sortable()` | `string` | `True` |  |
| `.state()` | `object` | **required** | Override the displayed value: ``lambda record: ...``. |

### `ImageColumn`
**Label:** Image
**Category:** column

| Setter | Type | Default | Description |
|---|---|---|---|
| `.align()` | `string` | **required** |  |
| `.allow_html()` | `boolean` | `True` |  |
| `.label()` | `string` | **required** |  |
| `.limit()` | `number` | **required** |  |
| `.rounded()` | `boolean` | `True` |  |
| `.searchable()` | `string` | `True` |  |
| `.sortable()` | `string` | `True` |  |
| `.state()` | `object` | **required** | Override the displayed value: ``lambda record: ...``. |
| `.thumbnail()` | `list` | **required** |  |

### `TextColumn`
**Label:** Text
**Category:** column

| Setter | Type | Default | Description |
|---|---|---|---|
| `.align()` | `string` | **required** |  |
| `.allow_html()` | `boolean` | `True` |  |
| `.label()` | `string` | **required** |  |
| `.limit()` | `number` | **required** |  |
| `.searchable()` | `string` | `True` |  |
| `.sortable()` | `string` | `True` |  |
| `.state()` | `object` | **required** | Override the displayed value: ``lambda record: ...``. |

## Table Filters

### `BooleanFilter`
**Label:** Boolean filter
**Category:** filter

| Setter | Type | Default | Description |
|---|---|---|---|
| `.field()` | `string` | **required** |  |
| `.label()` | `string` | **required** |  |

### `Filter`
**Label:** Text filter
**Category:** filter

| Setter | Type | Default | Description |
|---|---|---|---|
| `.field()` | `string` | **required** |  |
| `.label()` | `string` | **required** |  |

### `SelectFilter`
**Label:** Select filter
**Category:** filter

| Setter | Type | Default | Description |
|---|---|---|---|
| `.field()` | `string` | **required** |  |
| `.label()` | `string` | **required** |  |
| `.options()` | `object` | **required** |  |

### `TernaryFilter`
**Label:** Yes / No / Any
**Category:** filter

| Setter | Type | Default | Description |
|---|---|---|---|
| `.field()` | `string` | **required** |  |
| `.label()` | `string` | **required** |  |

## UI Blocks

### `AppShell`
**Label:** App shell
**Category:** block
> Root page frame: ``topbar`` / ``sidebar`` / ``content`` / ``footer``.

| Setter | Type | Default | Description |
|---|---|---|---|
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.sidebar_width()` | `string` | **required** |  |
| `.visible()` | `unknown` | **required** |  |

### `Card`
**Category:** block
> A bordered surface with optional header and footer slots.

| Setter | Type | Default | Description |
|---|---|---|---|
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.title()` | `string` | **required** |  |
| `.visible()` | `unknown` | **required** |  |

### `Column`
**Category:** block
> A grid child spanning ``span`` tracks (of its parent :class:`Grid`).

| Setter | Type | Default | Description |
|---|---|---|---|
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.offset()` | `number` | **required** |  |
| `.span()` | `number` | **required** |  |
| `.visible()` | `unknown` | **required** |  |

### `Divider`
**Category:** block
> A horizontal rule. No children.

| Setter | Type | Default | Description |
|---|---|---|---|
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.visible()` | `unknown` | **required** |  |

### `Footer`
**Category:** block
> A page footer.

| Setter | Type | Default | Description |
|---|---|---|---|
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.visible()` | `unknown` | **required** |  |

### `GlobalSearch`
**Label:** Global search
**Category:** block
> A top-bar search input. On input it ``GET``s ``endpoint`` with ``?q=``

| Setter | Type | Default | Description |
|---|---|---|---|
| `.endpoint()` | `string` | **required** | A URL path or URL name that returns an HTML results fragment. |
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.visible()` | `unknown` | **required** |  |

### `Grid`
**Category:** block
> A CSS grid - ``cols`` tracks, ``gap`` spacing. Children are usually

| Setter | Type | Default | Description |
|---|---|---|---|
| `.cols()` | `number` | **required** |  |
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.gap()` | `string` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.visible()` | `unknown` | **required** |  |

### `NavAction`
**Label:** Nav action
**Category:** nav
> A muted call-to-action row - ``+ Add new project``.

| Setter | Type | Default | Description |
|---|---|---|---|
| `.active()` | `boolean` | **required** | Force the active state (the panel passes its own computed value). |
| `.badge()` | `object` | **required** |  |
| `.dot()` | `string` | **required** | A CSS colour for a leading square (project-swatch style). |
| `.external()` | `boolean` | `True` |  |
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.icon()` | `string` | **required** |  |
| `.image()` | `string` | **required** | A logo / avatar URL shown in place of the icon. |
| `.image_alt()` | `string` | **required** |  |
| `.label()` | `object` | **required** |  |
| `.to()` | `string` | **required** | A URL path, an anchor, or a URL name. |
| `.visible()` | `unknown` | **required** |  |

### `NavDivider`
**Label:** Nav divider
**Category:** nav
> A horizontal rule between nav sections.

| Setter | Type | Default | Description |
|---|---|---|---|
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.visible()` | `unknown` | **required** |  |

### `NavGroup`
**Label:** Nav group
**Category:** nav
> A collapsible section. Its ``<button>`` toggles the child list;

| Setter | Type | Default | Description |
|---|---|---|---|
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.icon()` | `string` | **required** |  |
| `.id()` | `string` | **required** |  |
| `.image()` | `string` | **required** | A logo URL shown in place of the icon. |
| `.image_alt()` | `string` | **required** |  |
| `.label()` | `object` | **required** |  |
| `.open()` | `boolean` | `True` | Start expanded (unless the viewer already toggled it). |
| `.visible()` | `unknown` | **required** |  |

### `NavHeading`
**Label:** Nav heading
**Category:** nav
> A non-interactive section label.

| Setter | Type | Default | Description |
|---|---|---|---|
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.label()` | `object` | **required** |  |
| `.visible()` | `unknown` | **required** |  |

### `NavLink`
**Label:** Nav link
**Category:** nav
> One navigation entry - an ``<a>`` with an optional icon, count badge and

| Setter | Type | Default | Description |
|---|---|---|---|
| `.active()` | `boolean` | **required** | Force the active state (the panel passes its own computed value). |
| `.badge()` | `object` | **required** |  |
| `.dot()` | `string` | **required** | A CSS colour for a leading square (project-swatch style). |
| `.external()` | `boolean` | `True` |  |
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.icon()` | `string` | **required** |  |
| `.image()` | `string` | **required** | A logo / avatar URL shown in place of the icon. |
| `.image_alt()` | `string` | **required** |  |
| `.label()` | `object` | **required** |  |
| `.to()` | `string` | **required** | A URL path, an anchor, or a URL name. |
| `.visible()` | `unknown` | **required** |  |

### `NavUser`
**Label:** Nav user
**Category:** nav
> An account card pinned in the sidebar footer, with an optional menu.

| Setter | Type | Default | Description |
|---|---|---|---|
| `.avatar()` | `string` | **required** |  |
| `.email()` | `object` | **required** |  |
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.label()` | `object` | **required** | The display name (``name`` is the :class:`Component` identity property, |
| `.menu()` | `list` | **required** | ``[(label, url_or_name), ...]``. |
| `.visible()` | `unknown` | **required** |  |

### `Navbar`
**Category:** block
> A horizontal bar with a leading and a trailing region.

| Setter | Type | Default | Description |
|---|---|---|---|
| `.brand()` | `string` | **required** |  |
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.visible()` | `unknown` | **required** |  |

### `NotificationBell`
**Label:** Notification bell
**Category:** block
> A bell that polls an endpoint for the unread count and shows recent

| Setter | Type | Default | Description |
|---|---|---|---|
| `.endpoint()` | `string` | **required** |  |
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.interval()` | `number` | **required** |  |
| `.visible()` | `unknown` | **required** |  |

### `PageShell`
**Label:** Page shell
**Category:** block
> A page: a generated header (unless the ``header`` slot is filled) over a

| Setter | Type | Default | Description |
|---|---|---|---|
| `.accent()` | `string` | **required** | A CSS colour for the eyebrow / header rule (``--dcc-page-accent``). |
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.eyebrow()` | `object` | **required** | A short label above the title (a family / section tag). |
| `.hidden()` | `unknown` | **required** |  |
| `.summary()` | `object` | **required** |  |
| `.title()` | `object` | **required** |  |
| `.visible()` | `unknown` | **required** |  |

### `Prose`
**Category:** block
> A block of authored rich text. ``.html(...)`` is code-only - a stored

| Setter | Type | Default | Description |
|---|---|---|---|
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.html()` | `string` | **required** |  |
| `.visible()` | `unknown` | **required** |  |

### `Row`
**Category:** block
> Horizontal flow with wrap / alignment / justification.

| Setter | Type | Default | Description |
|---|---|---|---|
| `.align()` | `string` | **required** |  |
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.gap()` | `string` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.justify()` | `string` | **required** |  |
| `.visible()` | `unknown` | **required** |  |
| `.wrap()` | `boolean` | `True` |  |

### `Sidebar`
**Category:** block
> A vertical nav column. ``default`` holds the scrolling nav list (nav

| Setter | Type | Default | Description |
|---|---|---|---|
| `.brand()` | `string` | **required** |  |
| `.brand_icon()` | `string` | **required** |  |
| `.brand_image()` | `string` | **required** | A logo image URL shown in place of ``brand_icon``. |
| `.brand_image_alt()` | `string` | **required** |  |
| `.brand_url()` | `string` | **required** | A URL path or URL name - the brand becomes a link. |
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.searchable()` | `boolean` | `True` |  |
| `.visible()` | `unknown` | **required** |  |

### `Spacer`
**Category:** block
> Fixed vertical whitespace. ``size`` is one of none/sm/md/lg/xl.

| Setter | Type | Default | Description |
|---|---|---|---|
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.size()` | `string` | **required** |  |
| `.visible()` | `unknown` | **required** |  |

### `Stack`
**Category:** block
> Vertical flow. ``gap`` is one of none/sm/md/lg/xl.

| Setter | Type | Default | Description |
|---|---|---|---|
| `.align()` | `string` | **required** |  |
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.gap()` | `string` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.visible()` | `unknown` | **required** |  |

### `ThemeToggle`
**Label:** Theme toggle
**Category:** nav
> The light / dark / auto cycle button. Renders inside a ``dccShell``

| Setter | Type | Default | Description |
|---|---|---|---|
| `.extra_attributes()` | `keyvalue` | **required** |  |
| `.hidden()` | `unknown` | **required** |  |
| `.visible()` | `unknown` | **required** |  |
