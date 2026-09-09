"""Grep-as-test guardrails. Cheap, and they catch regressions no unit test would."""

from __future__ import annotations

import pathlib
import re

import django_control_components

ROOT = pathlib.Path(django_control_components.__file__).parent
TEMPLATES = ROOT / "templates"


def _template_files():
    return list(TEMPLATES.rglob("*.html"))


def test_no_literal_hx_attributes_in_templates():
    """Every hx-* must come from htmx.py so the htmx-4 migration is one file."""
    tokens = ("hx-get", "hx-post", "hx-put", "hx-patch", "hx-delete", "hx-target", "hx-swap")
    offenders = []
    for path in _template_files():
        text = path.read_text()
        for token in tokens:
            if token in text:
                offenders.append(f"{path.relative_to(ROOT)}: {token}")
    assert not offenders, offenders


def test_no_hand_rolled_buttons_outside_primitives():
    """Buttons come from the `ui` layer (or a cotton wrapper of it), not ad-hoc
    ``<button class="dcc-btn">`` per template. A handful of component-internal
    Alpine controls carry their own class and are exempt."""
    exempt = {
        "templates/cotton/dcc/button.html",
        "templates/cotton/dcc/modal.html",
        "templates/django_control_components/ui/button.html",
        "templates/django_control_components/ui/menu.html",
        "templates/django_control_components/ui/modal.html",
        # component-internal controls with their own class (not dcc-btn)
        "templates/django_control_components/controls/select.html",
        "templates/django_control_components/controls/password.html",
        "templates/django_control_components/layout/tabs.html",
        # client-side sort header toggle - bare button, no dcc-btn
        "templates/django_control_components/tables/_content.html",
    }
    offenders = []
    for path in _template_files():
        rel = str(path.relative_to(ROOT))
        if rel in exempt:
            continue
        if 'class="dcc-btn' in path.read_text():
            offenders.append(rel)
    assert not offenders, offenders


#: (template, variable) pairs allowed to interpolate into a line carrying
#: ``x-data``. Escaping does not defend an Alpine expression context - the HTML
#: parser decodes entities before Alpine reads the attribute - so each variable
#: here must be proven safe *pre-escape* at its source, not merely escaped.
ALPINE_INTERPOLATION_ALLOWLIST = {
    # slug_id() -> [A-Za-z0-9_-]
    "templates/django_control_components/panels/widgets/chart.html": {"payload_id"},
    "templates/django_control_components/tables/_content.html": {"config_id"},
    "templates/django_control_components/tables/table.html": {"table_id"},
    # md5 hex digest
    "templates/django_control_components/blocks/nav_group.html": {"group_id"},
    # a validated model field name
    "templates/django_control_components/controls/select.html": {"data_id"},
    # not inside the x-data value: a CSS length sanitised by _clean_len()
    "templates/django_control_components/blocks/app_shell.html": {"sidebar_width"},
    # server-compiled VisibilityRule expression, never a raw config string
    "templates/django_control_components/layout/tabs.html": {"visible_expr"},
}

_TEMPLATE_VAR = re.compile(r"\{\{\s*([a-zA-Z_][\w.]*)")


def test_no_django_interpolation_inside_alpine_data():
    """No unvetted {{ }} on an x-data line - that is the JS-injection footgun."""
    offenders = []
    for path in _template_files():
        rel = str(path.relative_to(ROOT))
        allowed = ALPINE_INTERPOLATION_ALLOWLIST.get(rel, set())
        for line in path.read_text().splitlines():
            if "x-data=" not in line or "{{" not in line:
                continue
            for var in _TEMPLATE_VAR.findall(line):
                if var not in allowed:
                    offenders.append(f"{rel}: {var} in {line.strip()}")
    assert not offenders, offenders


def test_mark_safe_only_at_reviewed_sites():
    allowed = {
        "core/attributes.py",
        "templatetags/dcc_tags.py",
        "schemas/schema.py",
        "schemas/layout.py",
        "blocks/base.py",  # Block.render_slot - same already-safe-parts concat as layout.py
        "tables/columns.py",  # .allow_html() - documented opt-in, escaping is default
        "icons/fontawesome.py",  # fixed markup + a setting-controlled asset URL
    }
    offenders = []
    for path in ROOT.rglob("*.py"):
        rel = str(path.relative_to(ROOT))
        if rel in allowed:
            continue
        text = path.read_text()
        if "mark_safe(" in text or "mark_safe (" in text:
            offenders.append(rel)
    assert not offenders, offenders
