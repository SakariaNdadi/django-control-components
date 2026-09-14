# HTMX compatibility policy

DCC currently supports and emits assets for HTMX 2. HTMX 4 remains a prerelease,
so it is not a production target for `0.1.0`. Host applications may disable the
managed HTMX asset with `{% dcc_assets htmx=False %}`, but a host-supplied version
is responsible for satisfying this contract.

## Stable DCC contract

- Templates do not contain literal `hx-*` attributes.
- Python creates request attributes through `django_control_components.htmx`.
- DCC endpoints return ordinary Django responses and must remain usable by a
  full-page, non-JavaScript request wherever progressive enhancement is promised.
- Application behavior should use `dcc:*` browser events rather than depending
  on version-specific HTMX lifecycle event names.

The invariant test in `tests/test_invariants.py` enforces the first rule.

## HTMX 4 adoption gates

1. Keep HTMX 2 as the managed default through the `0.1` line.
2. Run HTMX 4 as a non-blocking browser-test matrix entry while it is prerelease.
3. Track attribute, request-header, response-header, event, swap, redirect,
   history, error-status, cancellation, upload, and extension differences in the
   adapter and tests—not in component templates.
4. Test the official HTMX 2 compatibility extension only as a temporary bridge.
5. After HTMX 4 is stable, require the complete contract suite before declaring
   support in a DCC minor release.
6. Support HTMX 2 and 4 for at least one DCC minor-release cycle before changing
   the default.
7. Remove compatibility behavior only in a documented breaking DCC release.

The upstream prerelease and compatibility assets are published on the
[official HTMX releases page](https://github.com/bigskysoftware/htmx/releases).

## Required dual-version browser scenarios

- tables: search, filters, sorting, pagination, infinite loading, and history;
- schemas: live validation, CSRF failure, focus restoration, and file upload;
- actions: modal GET/POST, confirmation, redirects, 4xx/5xx handling, and refresh events;
- wizards: step swaps, validation failure, back/forward navigation;
- shell: out-of-band messages and notification refresh;
- request cancellation and repeated/overlapping requests.

Assertions must target final DOM state, URL, focus, and server requests rather
than private HTMX implementation details.
