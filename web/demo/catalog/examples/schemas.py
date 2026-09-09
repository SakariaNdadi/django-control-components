"""Catalog pages for ``django_control_components.schemas`` fields/layout."""

from __future__ import annotations

from django import forms

from django_control_components.schemas import (
    FileUpload,
    Fieldset,
    Grid,
    MultiSelect,
    Radio,
    Schema,
    Section,
    Select,
    Tab,
    Tabs,
    Textarea,
    TextInput,
    Toggle,
)

from ..page import ComponentExample, ComponentPageSpec


class _DemoForm(forms.Form):
    title = forms.CharField(required=True)
    body = forms.CharField(required=False, widget=forms.Textarea)
    status = forms.ChoiceField(
        choices=[("draft", "Draft"), ("live", "Live"), ("archived", "Archived")], required=False
    )
    tags = forms.MultipleChoiceField(
        choices=[("py", "Python"), ("js", "JS"), ("go", "Go")], required=False
    )
    featured = forms.BooleanField(required=False)
    plan = forms.ChoiceField(choices=[("free", "Free"), ("pro", "Pro")], required=False)


def _schema_html(request, build):
    return build().form(_DemoForm).strict().render(request=request)


SCHEMA = ComponentPageSpec(
    slug="schema",
    title="Schema",
    family="schemas",
    icon="list-check",
    summary=(
        "The full builder: decorates a Django Form/ModelForm - a schema never "
        "validates, the form does."
    ),
    examples=[
        ComponentExample(
            title="Full example",
            code=(
                "Schema.make().form(TaskForm).schema([\n"
                '    Section.make("Task").columns(2).schema([\n'
                '        TextInput.make("title").required().column_span_full(),\n'
                '        Select.make("status"),\n'
                '        Toggle.make("featured"),\n'
                "    ]),\n"
                "])"
            ),
            build=lambda request: _schema_html(
                request,
                lambda: Schema.make().schema(
                    [
                        Section.make("Task")
                        .columns(2)
                        .schema(
                            [
                                TextInput.make("title").required().column_span_full(),
                                Select.make("status"),
                                Toggle.make("featured"),
                            ]
                        )
                    ]
                ),
            ),
        ),
    ],
    props_table=[
        (".form(FormClass)", "type[Form]", "decorate a hand-written Form/ModelForm"),
        (".model(Model, fields=...)", "type[Model]", "builds a ModelForm via modelform_factory"),
        (".schema([...])", "list[Component]", "the field/layout tree (alias: .components())"),
        (".strict(bool=True)", "bool", "render only the fields you declared"),
        (".render(request=, form=)", "SafeString", "fields only - you supply <form>"),
        (".render_form(...)", "SafeString", "a complete <form> incl. CSRF"),
    ],
)

TEXT_INPUT = ComponentPageSpec(
    slug="text-input",
    title="Text Input",
    family="schemas",
    icon="font",
    summary="A single-line text field.",
    examples=[
        ComponentExample(
            title="Basic",
            code='Schema.make().form(DemoForm).schema([TextInput.make("title").required()])',
            build=lambda request: _schema_html(
                request, lambda: Schema.make().schema([TextInput.make("title").required()])
            ),
        ),
    ],
)

TEXTAREA = ComponentPageSpec(
    slug="textarea",
    title="Textarea",
    family="schemas",
    icon="align-left",
    summary="Multi-line text.",
    examples=[
        ComponentExample(
            title="Basic",
            code='Schema.make().form(DemoForm).schema([Textarea.make("body").column_span_full()])',
            build=lambda request: _schema_html(
                request, lambda: Schema.make().schema([Textarea.make("body").column_span_full()])
            ),
        ),
    ],
)

TOGGLE = ComponentPageSpec(
    slug="toggle",
    title="Toggle",
    family="schemas",
    icon="toggle-on",
    summary="A Checkbox subclass rendered as a switch.",
    examples=[
        ComponentExample(
            title="Basic",
            code='Schema.make().form(DemoForm).schema([Toggle.make("featured")])',
            build=lambda request: _schema_html(
                request, lambda: Schema.make().schema([Toggle.make("featured")])
            ),
        ),
    ],
)

SELECT = ComponentPageSpec(
    slug="select",
    title="Select",
    family="schemas",
    icon="caret-down",
    summary="Single choice.",
    examples=[
        ComponentExample(
            title="Searchable",
            code='Schema.make().form(DemoForm).schema([Select.make("status").searchable()])',
            build=lambda request: _schema_html(
                request, lambda: Schema.make().schema([Select.make("status").searchable()])
            ),
        ),
    ],
)

MULTI_SELECT = ComponentPageSpec(
    slug="multi-select",
    title="Multi Select",
    family="schemas",
    icon="list-check",
    summary="Multiple choice. .searchable() defaults to True.",
    examples=[
        ComponentExample(
            title="Basic",
            code='Schema.make().form(DemoForm).schema([MultiSelect.make("tags")])',
            build=lambda request: _schema_html(
                request, lambda: Schema.make().schema([MultiSelect.make("tags")])
            ),
        ),
    ],
)

RADIO = ComponentPageSpec(
    slug="radio",
    title="Radio",
    family="schemas",
    icon="circle-dot",
    summary="Single choice as a radio group.",
    examples=[
        ComponentExample(
            title="Basic",
            code='Schema.make().form(DemoForm).schema([Radio.make("plan")])',
            build=lambda request: _schema_html(
                request, lambda: Schema.make().schema([Radio.make("plan")])
            ),
        ),
    ],
)

FILE_UPLOAD = ComponentPageSpec(
    slug="file-upload",
    title="File Upload",
    family="schemas",
    icon="upload",
    summary="An image-aware upload field with resize/convert/strip-exif.",
    examples=[
        ComponentExample(
            title="Image field",
            code=(
                'FileUpload.make("cover").image()\n'
                '    .max_size("2mb").max_dimensions(2000, 2000).convert("webp")'
            ),
            note="Rendered standalone (no bound form field) - upload UI only.",
            build=lambda request: (
                FileUpload.make("cover")
                .image()
                .max_size("2mb")
                .max_dimensions(2000, 2000)
                .convert("webp")
            ),
        ),
    ],
)

SECTION = ComponentPageSpec(
    slug="section",
    title="Section",
    family="schemas",
    icon="square",
    summary="A titled block of fields.",
    examples=[
        ComponentExample(
            title="Basic",
            code=(
                "Schema.make().form(DemoForm).schema([\n"
                '    Section.make("Content").columns(2).schema([\n'
                '        TextInput.make("title").required(),\n'
                '        Toggle.make("featured"),\n'
                "    ])\n"
                "])"
            ),
            build=lambda request: _schema_html(
                request,
                lambda: Schema.make().schema(
                    [
                        Section.make("Content")
                        .columns(2)
                        .schema([TextInput.make("title").required(), Toggle.make("featured")])
                    ]
                ),
            ),
        ),
    ],
)

GRID = ComponentPageSpec(
    slug="grid-field",
    title="Grid (form layout)",
    family="schemas",
    icon="table-cells",
    summary="A column grid for fields.",
    examples=[
        ComponentExample(
            title="Basic",
            code=(
                "Grid.make().columns(2).schema([\n"
                '    Select.make("status"), TextInput.make("title"),\n'
                "])"
            ),
            build=lambda request: _schema_html(
                request,
                lambda: Schema.make().schema(
                    [
                        Grid.make()
                        .columns(2)
                        .schema([Select.make("status"), TextInput.make("title")])
                    ]
                ),
            ),
        ),
    ],
)

FIELDSET = ComponentPageSpec(
    slug="fieldset",
    title="Fieldset",
    family="schemas",
    icon="border-all",
    summary="Renders as a <fieldset>.",
    examples=[
        ComponentExample(
            title="Basic",
            code='Fieldset.make().columns(1).schema([TextInput.make("title")])',
            build=lambda request: _schema_html(
                request,
                lambda: Schema.make().schema(
                    [Fieldset.make().columns(1).schema([TextInput.make("title")])]
                ),
            ),
        ),
    ],
)

TABS = ComponentPageSpec(
    slug="tabs",
    title="Tabs",
    family="schemas",
    icon="folder-tree",
    summary="A tab strip + panels. .schema() accepts only Tab instances.",
    examples=[
        ComponentExample(
            title="Basic",
            code=(
                "Tabs.make().schema([\n"
                '    Tab.make("Content").schema([TextInput.make("title")]),\n'
                '    Tab.make("Settings").schema([Toggle.make("featured")]),\n'
                "])"
            ),
            build=lambda request: _schema_html(
                request,
                lambda: Schema.make().schema(
                    [
                        Tabs.make().schema(
                            [
                                Tab.make("Content").schema([TextInput.make("title")]),
                                Tab.make("Settings").schema([Toggle.make("featured")]),
                            ]
                        )
                    ]
                ),
            ),
        ),
    ],
)

PAGES = [
    SCHEMA,
    TEXT_INPUT,
    TEXTAREA,
    TOGGLE,
    SELECT,
    MULTI_SELECT,
    RADIO,
    FILE_UPLOAD,
    SECTION,
    GRID,
    FIELDSET,
    TABS,
]
