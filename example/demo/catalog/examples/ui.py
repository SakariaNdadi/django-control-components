"""Catalog pages for ``django_control_components.ui`` primitives."""

from __future__ import annotations

from django.utils.safestring import mark_safe

from django_control_components.core.context import RenderContext
from django_control_components.ui import Badge, Button, Checkbox, Icon, IconButton, Menu, Modal

from ..page import ComponentExample, ComponentPageSpec


def _row(request, *components):
    """Render several plain ``Component``s (not ``Block``s - a ``Row``'s
    slot only accepts ``Block`` children) side by side as one preview."""
    ctx = RenderContext(request=request)
    return mark_safe(
        '<div style="display:flex;gap:.5rem;flex-wrap:wrap">'
        + "".join(str(component.render(ctx)) for component in components)
        + "</div>"
    )


BUTTON = ComponentPageSpec(
    slug="button",
    title="Button",
    family="ui",
    icon="square",
    summary="The one button. Renders <a> when given .href(...), else <button>.",
    examples=[
        ComponentExample(
            title="Variants",
            code=(
                'Button.make().label("Save").variant("primary")\n'
                'Button.make().label("Cancel").variant("ghost")\n'
                'Button.make().label("Delete").variant("danger")'
            ),
            build=lambda request: _row(
                request,
                Button.make().label("Save").variant("primary"),
                Button.make().label("Cancel").variant("ghost"),
                Button.make().label("Delete").variant("danger"),
            ),
        ),
        ComponentExample(
            title="IconButton",
            code='IconButton.make().icon("trash").label("Delete").variant("danger")',
            build=lambda request: IconButton.make().icon("trash").label("Delete").variant("danger"),
        ),
    ],
    props_table=[
        (".label(str)", "str", "None/False render empty"),
        (".icon(name)", "str", "icon left of the label"),
        (".variant(str)", "str", "primary | secondary | danger | ghost | link"),
        (".size(str)", "str", "only sm is styled"),
        (".href(url)", "str", "renders as <a> instead of <button>"),
        (".type(str)", "str", "button (default) | submit | reset"),
        (".disabled()", "bool", ""),
    ],
)

BADGE = ComponentPageSpec(
    slug="badge",
    title="Badge",
    family="ui",
    icon="tag",
    summary="A small status pill.",
    examples=[
        ComponentExample(
            title="Variants",
            code=(
                'Badge.make().label("Live").variant("success")\n'
                'Badge.make().label("Draft").variant("muted")\n'
                'Badge.make().label("Error").variant("danger")'
            ),
            build=lambda request: _row(
                request,
                Badge.make().label("Live").variant("success"),
                Badge.make().label("Draft").variant("muted"),
                Badge.make().label("Error").variant("danger"),
            ),
        ),
    ],
    props_table=[
        (".label(str)", "str", "auto-escaped"),
        (".variant(str)", "str", "any string -> dcc-badge--<variant>"),
        (".icon(name)", "str", ""),
    ],
)

ICON = ComponentPageSpec(
    slug="icon",
    title="Icon",
    family="ui",
    icon="icons",
    summary="Renders through the active icon set. The name is positional.",
    examples=[
        ComponentExample(
            title="Basic",
            code='Icon.make("rocket").css_class("text-lg")',
            build=lambda request: Icon.make("rocket").css_class("text-lg"),
        ),
    ],
    props_table=[(".css_class(str)", "str", "the only setter")],
)

CHECKBOX = ComponentPageSpec(
    slug="checkbox-ui",
    title="Checkbox",
    family="ui",
    icon="square-check",
    summary="A standalone labelled checkbox (not the schema field).",
    examples=[
        ComponentExample(
            title="Checked",
            code='Checkbox.make().label("Featured").value("on").checked()',
            build=lambda request: Checkbox.make().label("Featured").value("on").checked(),
        ),
    ],
    props_table=[
        (".label(str)", "str", ""),
        (".value(str)", "str", ""),
        (".checked(bool=True)", "bool", ""),
    ],
)

MENU = ComponentPageSpec(
    slug="menu",
    title="Menu",
    family="ui",
    icon="ellipsis-vertical",
    summary="An Alpine disclosure over a list of pre-rendered HTML item strings.",
    examples=[
        ComponentExample(
            title="Basic",
            code=(
                'Menu.make().icon("ellipsis-vertical").align("end").items([\n'
                "    '<button class=\"dcc-menu__item\">Edit</button>',\n"
                "    '<button class=\"dcc-menu__item\">Delete</button>',\n"
                "])"
            ),
            build=lambda request: (
                Menu.make()
                .icon("ellipsis-vertical")
                .align("end")
                .items(
                    [
                        '<button type="button" class="dcc-menu__item">Edit</button>',
                        '<button type="button" class="dcc-menu__item">Delete</button>',
                    ]
                )
            ),
        ),
    ],
    props_table=[
        (".label(str)", "str", "trigger text"),
        (".icon(name)", "str", "default ellipsis-vertical"),
        (".items([str, ...])", "list[str]", "pre-rendered HTML, no slot"),
        (".align(str)", "str", "start | end (default end)"),
    ],
)

MODAL = ComponentPageSpec(
    slug="modal",
    title="Modal",
    family="ui",
    icon="window-restore",
    summary="A teleported overlay with a focus trap. The body is pre-rendered HTML.",
    examples=[
        ComponentExample(
            title="Static (open_on_load off, for preview)",
            code=(
                'Modal.make().heading("Confirm").size("sm")\n'
                '    .body("<p>Are you sure?</p>").open_on_load(False)'
            ),
            build=lambda request: (
                Modal.make()
                .heading("Confirm")
                .size("sm")
                .body("<p>Are you sure?</p>")
                .open_on_load(False)
            ),
        ),
    ],
    props_table=[
        (".heading(str)", "str", "header only renders when set"),
        (".size(str)", "str", "dcc-modal__dialog--<token>"),
        (".body(str)", "SafeString", "rendered |safe - caller owns escaping"),
        (".open_on_load(bool=True)", "bool", ""),
        (".dom_id(str)", "str", ""),
    ],
)

PAGES = [BUTTON, BADGE, ICON, CHECKBOX, MENU, MODAL]
