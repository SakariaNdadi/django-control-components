from __future__ import annotations

from django import forms

from django_control_components.infolists import (
    BadgeEntry,
    BooleanEntry,
    DateEntry,
    Infolist,
    TextEntry,
)
from django_control_components.panels import Resource
from django_control_components.schemas import (
    FileUpload,
    Schema,
    Section,
    Select,
    TextInput,
    Toggle,
)
from django_control_components.tables import (
    BadgeColumn,
    BooleanColumn,
    DateColumn,
    ImageColumn,
    SelectFilter,
    Table,
    TextColumn,
)

from ..models import Task
from ._base import ProsePage


class TaskForm(forms.ModelForm):
    """A ``TextInput`` field only renders as ``<input type="text">`` because
    it delegates to the bound Django widget - ``Schema.model(...)`` builds a
    plain ``modelform_factory`` with no widget overrides, which is why
    ``due_date`` fell back to a text box. An explicit widget here is the
    correct Django-level fix; nothing in the schema layer needs to know
    about dates specifically."""

    class Meta:
        model = Task
        fields = ["title", "priority", "done", "due_date", "cover"]
        widgets = {"due_date": forms.DateInput(attrs={"type": "date"})}


class TaskResource(Resource):
    """A demo resource with no real permission model behind it - open to
    every visitor rather than gated by Django model perms (the default
    ``Resource.can()``), since the whole point of this catalog is to be
    browsable without logging in."""

    model = Task
    navigation_icon = "list-check"
    create_redirect = "list"

    @classmethod
    def can(cls, request, action, obj=None):
        return True

    @classmethod
    def build_table(cls, *, request):
        return (
            Table.make(cls.get_queryset(request))
            .id("panel-tasks")
            .columns(
                [
                    ImageColumn.make("cover").thumbnail((32, 32)).rounded(),
                    TextColumn.make("title").sortable().searchable(),
                    BadgeColumn.make("priority").colors(
                        {"low": "muted", "medium": "secondary", "high": "danger"}
                    ),
                    BooleanColumn.make("done").labels(("✓", "-")),
                    DateColumn.make("due_date").since(),
                ]
            )
            .filters([SelectFilter.make("priority").options(Task.Priority.choices)])
            .default_sort("-due_date")
        )

    @classmethod
    def build_schema(cls, *, request):
        return (
            Schema.make()
            .form(TaskForm)
            .schema(
                [
                    Section.make("Task").schema(
                        [
                            TextInput.make("title").required(),
                            Select.make("priority"),
                            Toggle.make("done"),
                            FileUpload.make("cover").image(),
                        ]
                    ),
                    TextInput.make("due_date"),
                ]
            )
        )

    @classmethod
    def build_infolist(cls, *, request):
        return Infolist.make().schema(
            [
                TextEntry.make("title"),
                BadgeEntry.make("priority").colors(
                    {"low": "muted", "medium": "secondary", "high": "danger"}
                ),
                BooleanEntry.make("done"),
                DateEntry.make("due_date"),
            ]
        )


class FullExamplePage(ProsePage):
    template_name = "demo/pages/full_example.html"
    slug = "full-example"
    nav_label = "Full example"
    nav_icon = "diagram-project"
    nav_group = "Getting started"
    page_eyebrow = "Getting started"
    page_accent = "#b45309"
    page_title = "Full end-to-end example"
    page_summary = (
        "How a whole admin-independent CRUD surface is built in pure Python with "
        "Panel, Resource and the Table / Schema / Infolist builders."
    )

    def get_context_data(self, **kwargs):
        from django.urls import reverse

        ctx = super().get_context_data(**kwargs)
        ctx["tasks_url"] = reverse(f"{self.panel.namespace}:{TaskResource.slug()}-list")
        return ctx
