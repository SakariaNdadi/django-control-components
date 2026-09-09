"""Catalog pages for ``django_control_components.actions``."""

from __future__ import annotations

from types import SimpleNamespace

from django_control_components.actions import Action, BulkAction

from ..page import ComponentExample, ComponentPageSpec

_RECORD = SimpleNamespace(pk=1, title="Ship the release")


def _noop(record=None, records=None):
    return None


def _bound(action):
    action.bind_owner("demo-actions")
    return action


ACTION = ComponentPageSpec(
    slug="action",
    title="Action",
    family="actions",
    icon="bolt",
    summary="A named, addressable operation on one record.",
    examples=[
        ComponentExample(
            title="Confirm dialog",
            code=(
                'Action.make("publish").label("Publish").icon("rocket")\n'
                "    .requires_confirmation().action(lambda record: record.publish())"
            ),
            build=lambda request: _bound(
                Action.make("publish")
                .label("Publish")
                .icon("rocket")
                .requires_confirmation()
                .action(_noop)
            ).render_trigger(record=_RECORD, request=request),
        ),
        ComponentExample(
            title="Danger variant",
            code='Action.make("delete").label("Delete").variant("danger").requires_confirmation()',
            build=lambda request: _bound(
                Action.make("delete")
                .label("Delete")
                .variant("danger")
                .requires_confirmation()
                .action(_noop)
            ).render_trigger(record=_RECORD, request=request),
        ),
    ],
    props_table=[
        (".label(str)", "str", "default: title-cased name"),
        (".icon(name)", "str", ""),
        (".variant(str)", "str", "secondary (default) | primary | danger | ghost | link"),
        (".to_url(str|fn)", "str|fn", "render as a plain <a>"),
        (".requires_confirmation()", "-", "bare confirm dialog"),
        (".action(fn)", "callable", "the callback, run on POST"),
        (".authorize(perm|fn)", "str|fn", "checked at render and on POST"),
        (".collapsed()", "-", "fold into the trailing menu (table row actions)"),
    ],
)

BULK_ACTION = ComponentPageSpec(
    slug="bulk-action",
    title="Bulk Action",
    family="actions",
    icon="layer-group",
    summary="The same operation on many records - no single record.",
    examples=[
        ComponentExample(
            title="Basic",
            code=(
                'BulkAction.make("archive").label("Archive").requires_confirmation()\n'
                "    .action(lambda records: records.update(status='archived'))"
            ),
            build=lambda request: _bound(
                BulkAction.make("archive").label("Archive").requires_confirmation().action(_noop)
            ).render_trigger(request=request),
        ),
    ],
)

PAGES = [ACTION, BULK_ACTION]
