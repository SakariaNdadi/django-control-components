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
| `NavLink` | – | `.label` · `.icon(name)` · `.image(url)` / `.image_alt(str)` · `.to(url \| "#anchor" \| url_name)` · `.badge(str)` · `.dot(css_color)` · `.external()` · `.active(bool)` / `.active_for(prefix)` |
| `NavGroup` | `default` | `.label` · `.icon` · `.image(url)` / `.image_alt(str)` · `.id(str)` · `.open()` (start expanded) |
| `NavHeading` | – | `.label` |
| `NavDivider` | – | – |
| `NavAction` | – | same as `NavLink`; renders muted (a "+ Add …" row) |
| `NavUser` | – | `.name` · `.email` · `.avatar(url)` · `.menu([(label, url), …])` |
| `ThemeToggle` | – | – (cycles auto / light / dark; needs a `dccShell` scope, which `AppShell` and the panel shell provide) |

`.image(url)` shows a logo / avatar in place of the icon (`.image_alt` sets its
`alt`); `Sidebar.brand_image(url)` does the same for the brand mark, overriding
`.brand_icon(...)`. `.to()` takes a path, an anchor, or a URL name (reversed, a
miss → `#`).
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

### How it is on every page

`panels/base.html` (the shell every panel page extends) does
`{% include "django_control_components/panels/_nav.html" %}`, and that partial is
just `{% dcc_render sidebar %}`. Both context-data hooks -
`PanelPage.get_context_data` (dashboards, custom pages) and `_ResourcePage`'s
(list / create / edit / view / delete) - set
`ctx["sidebar"] = panel_sidebar(self.panel, self.request)`
(`panels/nav.py`). So a resource page, a dashboard, a custom `PanelPage` and the
studio nav preview all render the identical sidebar with no per-page code.

If you shadow `panels/base.html` in your own project, keep the
`{% include ".../_nav.html" %}` (or call `{% dcc_render sidebar %}` yourself) and
nothing else changes.

### Where the tree comes from - and permissions

`panel_sidebar` calls `build_nav(panel, request)`, which is **already
access-filtered** before any block is built:

- a code `Resource` entry is included only if `resource.can(request, "view")`
  is true (`panels/nav.py::_can_view_resource`);
- a stored `NavItem` is included only if `row.is_visible_to(user)` - the
  three-state `Visibility` (`public` / `auth` / `restricted`) plus
  `required_permission` and the `users` / groups grants;
- a studio spec / dashboard entry checks `DynamicResource.for_spec(spec).can(...)`.

`NavLink` and `NavGroup` themselves carry **no** authorization logic - by the
time the tree reaches them every hidden item is already gone. A blocked resource
still 403s if its URL is hit directly; the sidebar just doesn't advertise it.

### What the author declares

Unchanged: `Resource.navigation_group` / `navigation_icon`,
`PanelPage.nav_group` / `nav_icon` / `nav_label`. `panels/nav.py::nav_blocks`
turns each heading-with-children into a `NavGroup` (all start expanded; `dccNav`
persists any the viewer collapses), each bare item into a `NavLink`, and adds a
footer with a `ThemeToggle` and - when signed in - a `NavUser` card.

The sidebar can be collapsed to an icon rail (the `«` button, desktop) -
`dccShell.railed`, persisted to `localStorage`. It scrolls within itself
(`position: sticky; height: 100vh` on desktop, drawer on mobile).
