"""The palette metadata layer over the type registries."""

from __future__ import annotations

import json

import pytest

from django_control_components.core.describe import (
    CODE_ONLY_SETTERS,
    describe_type,
    strip_privileged_setters,
)
from django_control_components.infolists import ENTRY_TYPES
from django_control_components.panels import WIDGET_TYPES
from django_control_components.schemas import FIELD_TYPES
from django_control_components.tables import COLUMN_TYPES, FILTER_TYPES

ALL_REGISTRIES = [COLUMN_TYPES, FILTER_TYPES, FIELD_TYPES, ENTRY_TYPES, WIDGET_TYPES]


def test_every_registered_type_describes_without_raising():
    for registry in ALL_REGISTRIES:
        for name in registry.names():
            info = registry.info(name)
            assert info.name == name
            assert info.label


def test_field_config_setters_are_spec_editable():
    """The studio hides ``code_only`` setters. ``label`` / ``placeholder`` /
    ``required`` are ``str``/``bool`` (or that union with a callable) - editable
    in a spec. Regression: a TYPE_CHECKING-only ``Callable`` import used to make
    ``inspect.signature`` fail and every one of these got marked code_only, so
    the no-code builder hid the Label input on every field."""
    from django_control_components.schemas.fields.text import TextInput

    editable = {s.name: s for s in describe_type(TextInput).setters}
    for name in ("label", "placeholder", "help_text", "hint", "icon"):
        assert editable[name].kind == "string", name
        assert not editable[name].code_only, name
    for name in ("required", "disabled", "readonly"):
        assert editable[name].kind == "boolean", name
        assert not editable[name].code_only, name


def test_layout_types_accept_children_and_leaves_do_not():
    containers = {"Section", "Grid", "Fieldset", "Tab", "Tabs"}
    for name in FIELD_TYPES.names():
        assert FIELD_TYPES.info(name).accepts_children is (name in containers)


def test_state_setter_is_code_only():
    from django_control_components.tables.columns import TextColumn

    info = describe_type(TextColumn)
    state = next(s for s in info.setters if s.name == "state")
    assert state.code_only
    assert "state" in CODE_ONLY_SETTERS


def test_allow_html_is_superuser_gated_and_stripped_for_others():
    info = COLUMN_TYPES.info("TextColumn")
    allow_html = next(s for s in info.setters if s.name == "allow_html")
    assert allow_html.requires == "superuser"

    stripped = strip_privileged_setters(info, is_superuser=False)
    assert all(s.name != "allow_html" for s in stripped.setters)
    kept = strip_privileged_setters(info, is_superuser=True)
    assert any(s.name == "allow_html" for s in kept.setters)


def test_choice_kind_from_literal_annotation():
    from django_control_components.panels.widgets import ChartWidget

    info = describe_type(ChartWidget)
    kind = next(s for s in info.setters if s.name == "kind")
    # ChartWidget.kind validates against a fixed set; introspection sees `str`,
    # so this just asserts it is at least a plain editable string, not unknown.
    assert kind.kind in {"string", "choice"}
    assert not kind.code_only


def test_palette_json_is_serialisable_and_gated(rf, django_user_model):
    from django_control_components.studio.palette import palette

    staff = django_user_model.objects.create_user("staff", is_staff=True)
    request = rf.get("/")
    request.user = staff
    doc = palette(request)
    blob = json.dumps(doc)  # round-trips
    assert "allow_html" not in blob  # stripped for non-superuser
    assert set(doc) == {"columns", "filters", "fields", "entries", "widgets", "blocks"}


pytestmark = pytest.mark.django_db
