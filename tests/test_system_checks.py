"""Startup ``manage.py check`` validation of the ``DCC`` settings dict."""

from __future__ import annotations

import pytest

from django_control_components.apps import _check_settings, _check_unauthorized_actions

pytestmark = pytest.mark.django_db


def _ids(messages):
    return {m.id for m in messages}


def test_unauthorized_actions_warn_only_without_default_deny(settings):
    from django_control_components.actions.action import Action
    from django_control_components.panels import Panel, Resource
    from django_control_components.tables import Table, TextColumn
    from tests.testapp.models import Article

    class Widget(Resource):
        model = Article

        @classmethod
        def build_table(cls, *, request):
            return (
                Table.make(cls.get_queryset(request))
                .columns([TextColumn.make("title")])
                .actions([Action.make("nuke")])
            )

    Panel("checkpanel").path("checkpanel").resources([Widget])

    settings.DCC = {}
    assert "django_control_components.W013" in _ids(_check_unauthorized_actions(None))

    settings.DCC = {"ACTIONS_DEFAULT_DENY": True}
    assert _check_unauthorized_actions(None) == []


def test_clean_settings_pass(settings):
    settings.DCC = {"STUDIO_MODELS": ["testapp.article"]}
    assert _check_settings(None) == []


def test_unknown_key_is_flagged(settings):
    settings.DCC = {"STUDdIO_MODELS": []}
    assert "django_control_components.E010" in _ids(_check_settings(None))


def test_bad_icon_set_is_flagged(settings):
    settings.DCC = {"ICON_SET": "nope.NoSuchIconSet"}
    assert "django_control_components.E011" in _ids(_check_settings(None))


def test_unresolvable_studio_model_warns(settings):
    settings.DCC = {"STUDIO_MODELS": ["ghost.Nothing"]}
    assert "django_control_components.W011" in _ids(_check_settings(None))


def test_bad_studio_callable_warns(settings):
    settings.DCC = {"STUDIO_CALLABLES": {"x": "nope.not_a_func"}}
    assert "django_control_components.W012" in _ids(_check_settings(None))
