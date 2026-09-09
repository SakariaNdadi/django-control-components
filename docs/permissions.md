# Permissions

Six mechanisms, deliberately not layered into one. Each answers a different
question, and they compose by intersection - nothing here ever widens a Django
permission.

| # | Mechanism | Question it answers | Enforced |
|---|---|---|---|
| 1 | Panel guards | may this user open the panel at all? | dispatch |
| 2 | `Resource.can()` | may this user do `view`/`add`/`change`/`delete` here? | dispatch |
| 3 | `Visibility` (studio rows) | should this user *see* this item? | render + dispatch |
| 4 | Studio access | may this user open the builder? | dispatch |
| 5 | Action authorization | may this user run this action? | render + endpoint |
| 6 | `.visible()` / `.hidden()` | should this element be drawn? | render only - **not** authorization |

The invariant that ties them together, from `studio/access.py`:

> **The studio grants visibility, never authorization.** A `can_see` grant can
> only hide things; data access stays `Resource.can()` → `user.has_perm`.

## 1. Panel guards

A guard is `Callable[[HttpRequest], bool]`. Returning `False` denies with
`PermissionDenied` (403); raising `LoginRequired` redirects to the login page.
`LoginRequired` is deliberately **not** a `PermissionDenied` subclass, which is
what lets the page tell "sign in" apart from "you may not".

```python
from django_control_components.panels import Panel
from django_control_components.panels.guards import staff_required, group_required

panel = Panel("ops").path("ops").auth(staff_required, group_required("Operations"))
```

| guard | passes when |
|---|---|
| `login_required` | the user is authenticated |
| `staff_required` | authenticated **and** `is_staff` |
| `permission_required(perm)` | authenticated **and** `has_perm(perm)` |
| `group_required(*names)` | authenticated **and** in every named group (superusers bypass) |

All four raise `LoginRequired` for an anonymous request rather than returning
`False`, so an anonymous visitor is redirected instead of shown a 403.

Guards run in `Panel.check_access`, called from every panel page's `dispatch`.
**A panel with no `.auth(...)` is public** - resource pages are still gated by
mechanism 2, but a widget dashboard is not. Set a guard explicitly.

Custom guards are ordinary callables:

```python
def owns_a_shop(request):
    if not request.user.is_authenticated:
        raise LoginRequired
    return request.user.shops.exists()
```

## 2. Resource permissions

`Resource.can(request, action, obj=None)` resolves a standard Django permission:

```text
<app_label>.<action>_<model_name>        # e.g. blog.change_article
```

`permission_prefix` overrides the model-name half (and the app label too, when it
contains a dot). The action is always injected, so `view` / `add` / `change` /
`delete` stay four distinct permissions.

Resolution order: anonymous → `False`; superuser → `True`; then, when an object
is in hand, `user.has_perm(perm, obj)` gets first say - so an object-level backend
(django-guardian, rules) can grant - falling back to the model-level permission.
That fallback is what preserves plain-Django behaviour, since `ModelBackend`
returns `False` for every object-scoped check.

Every resource page checks this in `dispatch`, before any query the page renders.

## 3. Three-state visibility

Studio-stored rows (`DashboardSpec`, `PanelDashboard`, `NavItem`, `Page`) mix in
`AccessControlled`, which adds four fields: `visibility`, `groups`, `users`,
`required_permission`.

| `visibility` | audience |
|---|---|
| `public` | everyone, signed-out visitors included |
| `auth` | any signed-in user |
| `restricted` | only the listed groups / users, subject to `required_permission` |

`is_visible_to(user)` resolves **by explicit grant, never by deny**: `PUBLIC`
passes immediately; anonymous fails everything else; superuser passes; `AUTH`
passes; otherwise `required_permission` is a deny gate, then the `users` and
`groups` grants decide. An ungranted `restricted` row is invisible.

> **`restricted` is the default.** A row created in code without an explicit
> `visibility=` is invisible to everyone but superusers. This trips people up
> constantly - always set it.

```python
NavItem.objects.create(
    panel="ops", label="Runbook",
    target_kind=NavItem.Kind.URL, target="/runbook/",
    visibility="auth",          # without this, nobody sees it
)
```

Two query helpers, and the difference matters:

- `visible_queryset(qs, user)` - one query, for nav rendering. It **cannot**
  express `required_permission` in SQL, so it returns rows that carry one.
- `visible_list(qs, user)` - the same, with the `required_permission` deny gate
  re-applied in Python. Use this wherever the result is shown to the user
  directly rather than gated again by `is_visible_to`.

Edit these through the studio's roles screen, which is superuser-only.

## 4. Studio access

Opening any builder needs `dcc_studio.use_studio` (or superuser). `require_studio`
raises `LoginRequired` for anonymous and denies everyone else without it; every
studio view enforces it in `dispatch`.

Treat `use_studio` as a privileged grant, not a peer of "staff": a holder writes
page trees, dashboards, nav and resource specs that then render in other users'
browsers, superusers included. The studio is positioned as a dev-only tool, and
a system check (`dcc_studio.W003`) warns when it is installed with `DEBUG=False`.

## 5. Action authorization

`.authorize(rule)` takes a permission string or a callable:

```python
Action.make("publish").authorize("blog.change_article")
Action.make("archive").authorize(lambda user, record: record.owner_id == user.pk)
```

Checked in two places, and both matter:

- **render** - `render_trigger` returns an empty string and `row_click_attrs`
  returns `{}` when unauthorized, so the button is never drawn;
- **endpoint** - `ActionView` re-checks on both GET and POST and returns 403,
  after re-scoping the submitted record ids to the owner's own queryset. A
  tampered pk cannot reach a row the table does not expose.

Two baselines sit under that:

- An action with **no** `.authorize()` rule is implicitly allowed to any
  signed-in user. `ActionView` is mounted outside any panel, so it carries no
  guard of its own - it refuses an anonymous request to an unruled action
  outright. An action meant to be usable signed-out opts in with an explicit
  rule (`.authorize(lambda: True)`); an action that carries any rule is left to
  `is_authorized`.
- Set `DCC["ACTIONS_DEFAULT_DENY"] = True` to refuse an unruled action for
  everyone, signed-in included.

One interaction worth knowing: an unruled action on a page an anonymous visitor
can reach is still *drawn* for them (the render check passes) and only fails on
submit with a 403. Put a guard on the panel, or set `ACTIONS_DEFAULT_DENY`,
rather than relying on the endpoint being the only stop.

The system check `W013` warns for any action reachable from a resource table with
no `.authorize()` rule. It builds each table with an anonymous request to find
them, so it catches the common case, not every case - the registry is populated
at render time.

## 6. Presentation visibility is not authorization

`Component.visible()` / `.hidden()` / `.when()` and the client-side
`visible_when(...)` DSL decide whether an element is *drawn*. They are
presentation. Never use them to hide something a user must not reach.

For studio-stored block trees there **is** a server-side gate, separate from
those props:

```json
{"type": "Card", "perms": ["blog.view_article"], "when": "is_beta_tester"}
```

`perms` are ANDed through `has_perm` (superusers pass); `when` names an alias
from `DCC["STUDIO_CALLABLES"]`. The `visible` / `hidden` props are not consulted
there.

## Where each check fires

| Enforcement point | What runs |
|---|---|
| dispatch, panel-wide | `Panel.check_access` → your guards |
| dispatch, per resource + object | `Resource.can` |
| dispatch, studio builder | `require_studio` |
| dispatch, stored page | `resolve_page` - **404, not 403** |
| endpoint, actions | anonymous refusal on an unruled action, then `Action.is_authorized` |
| endpoint, live field validation | the schema's `authorize`, else "any signed-in user" |
| render, nav | `build_nav` drops items the user cannot reach |
| render, actions | `render_trigger` / `row_click_attrs` |
| render, stored blocks | `perms` / `when` gate |

A restricted stored page 404s rather than 403s on purpose: a 403 would confirm
the page exists.

Render-time filtering is advisory. It keeps users from being shown doors they
cannot open - it is not what keeps the doors locked. Every render-time drop above
has a dispatch- or endpoint-time counterpart, and that is the one enforcing.

## Where to go next

- [panels.md](panels.md) - mounting panels and resources
- [navigation.md](navigation.md) - how the nav applies these filters
- [actions.md](actions.md) - the full action lifecycle
- [settings.md](settings.md) - `ACTIONS_DEFAULT_DENY`, `STUDIO_CALLABLES`
