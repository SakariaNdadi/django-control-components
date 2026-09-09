# Navigation

The sidebar of a panel - and any nav column you build yourself - is composed
from small blocks. A live version of every one of these is at `/nav-link/`,
`/nav-group/`, `/nav-user/` in the bundled `web/` project; the demo panel's own
sidebar is built from them (`panels/nav.py::panel_sidebar`).

## `Sidebar`

```python
from django_control_components.blocks import Sidebar, NavLink, NavGroup, ThemeToggle, NavUser

(
    Sidebar()
    .brand("DCC").brand_icon("cubes").brand_url("dcc-panel-docs:index")
    .fill("default", [ ... nav blocks ... ])          # the scrolling list
    .fill("footer", [ThemeToggle(), NavUser().label("Ada")])  # pinned to the bottom
)
```

`slots`: `default` (scrolls), `footer` (pinned, border-top). It renders the same
`.dcc-panel__nav` markup the panel shell already styles, so the responsive drawer
(`dccShell`: hamburger + scrim at ≤48rem) works with no extra wiring.

## Nav blocks

| block | slots | setters |
|---|---|---|
| `NavLink` | – | `.label` · `.icon(name)` · `.to(url \| "#anchor" \| url_name)` · `.badge(str)` · `.dot(css_color)` · `.external()` · `.active(bool)` / `.active_for(prefix)` |
| `NavGroup` | `default` | `.label` · `.icon` · `.id(str)` · `.open()` (start expanded) |
| `NavHeading` | – | `.label` |
| `NavDivider` | – | – |
| `NavAction` | – | same as `NavLink`; renders muted (a "+ Add …" row) |
| `NavUser` | – | `.name` · `.email` · `.avatar(url)` · `.menu([(label, url), …])` |
| `ThemeToggle` | – | – (cycles auto / light / dark; needs a `dccShell` scope, which `AppShell` and the panel shell provide) |

`.to()` takes a path, an anchor, or a URL name (reversed, a miss → `#`).
`NavLink` derives its active state from `request.path` unless you pass
`.active(...)` explicitly - the panel does, from its own longest-prefix match.

## Collapsible groups (`dccNav`)

`NavGroup` renders a `<button aria-expanded aria-controls>` over a
`role="group"` sublist. The `dccNav` Alpine component holds the open state and
persists it per group id to `localStorage` (`dcc-nav-open`), so a section the
viewer collapses stays collapsed on the next visit. `.open()` sets the default
for a first-time viewer; a group that contains the active link opens
automatically when the panel builds the tree.

No `@alpinejs/collapse` plugin is used - the sublist toggles with `x-show` +
`x-transition`.

## Accessibility

- group button: `aria-expanded`, `aria-controls` → the sublist `id`;
- active link: `aria-current="page"`;
- `NavUser` menu: `role="menu"` / `role="menuitem"`, focus-trapped (`x-trap`,
  from the always-loaded `@alpinejs/focus`), `Esc` and outside-click close it;
- chevrons and colour dots are `aria-hidden`.

## The panel sidebar

A panel author changes nothing - `Resource.navigation_group` /
`PanelPage.nav_group` / `navigation_icon` still declare the tree. `panels/nav.py`
turns that tree into `NavGroup` / `NavLink` blocks (every section collapsible),
adds a footer with the theme toggle and - when signed in - a `NavUser` card, and
`panels/_nav.html` renders it with `{% dcc_render sidebar %}`.
