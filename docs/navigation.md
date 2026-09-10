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

`.searchable()` adds a client-side filter box above the list: typing narrows the
links (and auto-opens the groups that match); it hides when the sidebar is
railed. Purely presentational - it shows/hides `<li>`s, it never touches the nav
data. On a panel, turn it on with `Panel(...).sidebar_searchable()`.

## Nav blocks

| block | slots | setters |
|---|---|---|
| `NavLink` | – | `.label` · `.icon(name)` · `.image(url)` / `.image_alt(str)` · `.to(url \| "#anchor" \| url_name)` · `.badge(str)` · `.dot(css_color)` · `.external()` · `.active(bool)` / `.active_for(prefix)` |
| `NavGroup` | `default` | `.label` · `.icon` · `.image(url)` / `.image_alt(str)` · `.id(str)` · `.open()` (start expanded) |
| `NavHeading` | – | `.label` |
| `NavDivider` | – | – |
| `NavAction` | – | same as `NavLink`; renders muted (a "+ Add …" row) |
| `NavUser` | – | `.label` · `.email` · `.avatar(url)` · `.menu([(label, url), …])` |
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
persists each toggle to **both** `localStorage` and a `dcc-nav-open` cookie
(base64 JSON, one-year), so a section the viewer collapses stays collapsed on
the next visit. `.open()` sets the default; the panel builds every group
`.open()`, so a first-time viewer sees the whole tree expanded.

The cookie is what keeps navigation flicker-free: `NavGroup.get_view_data`
reads it and renders `data-default-open="0"` for a group the viewer collapsed,
and `.dcc-nav__group[data-default-open="0"] > .dcc-nav__sublist { display: none }`
in the shipped stylesheet collapses it from the first paint - Alpine has nothing
to hide on load. No `x-cloak`: with JS disabled the nav still renders (every
group open) and stays usable.

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

`panels/base.html` (the shell every panel page extends) renders the sidebar
inline with `{% dcc_render sidebar %}`. Both context-data hooks -
`PanelPage.get_context_data` (dashboards, custom pages) and `_ResourcePage`'s
(list / create / edit / view / delete) - set
`ctx["sidebar"] = panel_sidebar(self.panel, self.request)`
(`panels/nav.py`). So a resource page, a dashboard, a custom `PanelPage` and the
studio nav preview all render the identical sidebar with no per-page code.

If you shadow `panels/base.html` in your own project, keep the
`{% dcc_render sidebar %}` call and nothing else changes. (There is also a
`panels/_nav.html` partial wrapping the same call in an `{% if sidebar %}`; the
studio's nav preview uses it, and it works just as well in a shadowed base.)

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

### How the tree is built

`build_nav(panel, request)` is four steps:

1. **code nodes** - the resources and `PanelPage`s the panel was constructed
   with, plus any studio specs and dashboards, from `Panel.navigation(request)`;
2. **stored nodes** - `NavItem` rows for this panel, when the studio app is
   installed. If it is not, this step is skipped entirely;
3. **active marking** - the node whose URL is the longest prefix of
   `request.path` is marked active. Exactly one node wins;
4. **grouping** - flat `group=` strings are folded into heading nodes.

Ordering: stored rows sort by `(order, pk)`; code groups appear in the order
they are first seen. There is no global sort, so a code group and a stored group
do not interleave - code nodes come first.

Everything above produces `NavNode`s - a plain dataclass, not blocks. A node
with no URL and no `external` flag *is* a heading. `nav_blocks(tree)` turns that
into blocks, and `panel_sidebar(panel, request)` is just
`sidebar_from_tree(panel, build_nav(panel, request), request)`.

### Rendering the tree somewhere else

`sidebar_from_tree(panel, tree, request, *, footer=True)` is the seam. Pass it a
tree you built or filtered yourself:

```python
from django_control_components.panels.nav import build_nav, sidebar_from_tree

tree = [n for n in build_nav(panel, request) if n.label != "Admin"]
sidebar = sidebar_from_tree(panel, tree, request, footer=False)
```

`footer=False` drops the `ThemeToggle` / `NavUser` block - what the studio's nav
preview uses, since it renders inside a page that already has both.

If you have no `Panel` at all, skip this and build a `Sidebar` block directly -
see [integration.md](integration.md).

## Stored nav (`NavItem`)

With the studio installed, nav can also come from the database, edited in the nav
builder and merged into the tree after the code nodes.

| `target_kind` | `target` is | permission-checked |
|---|---|---|
| `group` | – (a heading) | – |
| `url` | a site-relative path or `http(s)://…` | – |
| `url_name` | a URL name to reverse | – |
| `resource` | a resource slug | yes - `view` |
| `spec` | a studio spec slug | yes - `view` |
| `page` | a stored `Page` | yes - visibility |
| `dashboard` | a dashboard slug | **no** - visibility only |

`dashboard` is the one target kind with no permission check beyond the row's own
`is_visible_to`. Its own view still authorizes on dispatch, so this is a "do not
treat the nav as the gate" caveat, not a hole.

Two model invariants, enforced in `clean()` and applied on every save:

- **nesting is capped at two levels**, with an ancestor cycle check;
- a `url` target must be site-relative or `http(s)` - which is what rejects
  `javascript:`.

Unresolvable targets vanish rather than erroring: a `NoReverseMatch`, a failed
permission check or a missing row yields an empty URL, and any non-group node
without a URL is dropped from the tree.

> `NavItem.visibility` defaults to `restricted`, so a row created in code with
> no `visibility=` is invisible to everyone but superusers. See
> [permissions.md](permissions.md).

```python
NavItem.objects.create(
    panel="ops", label="Runbook", order=10,
    target_kind=NavItem.Kind.URL, target="/runbook/",
    visibility="auth",
)
```

Concurrency: the sidebar is many rows, so a `NavDocument` row per panel carries a
`revision` counter. The nav builder posts the revision it loaded; a mismatch is a
409 carrying the server's copy, rather than a silent overwrite of someone else's
edit.

## Where to go next

- [permissions.md](permissions.md) - the filters applied to the tree
- [integration.md](integration.md) - a sidebar without a panel
- [blocks.md](blocks.md) - the block tree these are part of
