"""Hand-built pages for interactive behaviour the demo panel doesn't isolate.

Each view renders through ``e2e/base.html`` (the panel shell + ``{% dcc_assets %}``)
so Alpine and htmx are wired exactly as in a real panel.
"""

from __future__ import annotations

from django import forms
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt

from django_control_components.blocks import (
    GlobalSearch,
    NavGroup,
    NavLink,
    NotificationBell,
    Sidebar,
    ThemeToggle,
)
from django_control_components.core.context import RenderContext
from django_control_components.schemas import Schema, Section, Select, TextInput, Toggle
from django_control_components.ui import Menu, Modal

_NAV_PATH = "/e2e/nav/"


def _ctx(request: HttpRequest) -> RenderContext:
    return RenderContext(request=request)


def _doc(request: HttpRequest, body: str, *, sidebar: str = "", title: str = "e2e") -> HttpResponse:
    return render(
        request,
        "e2e/base.html",
        {"body": mark_safe(body), "sidebar": mark_safe(sidebar), "title": title},
    )


def _sidebar(request: HttpRequest, *, searchable: bool = False) -> str:
    builder = Sidebar().brand("E2E")
    if searchable:
        builder = builder.searchable()
    return str(
        builder.fill(
            "default",
            [
                NavGroup()
                .label("Alpha")
                .open()
                .fill(
                    "default",
                    [
                        NavLink().label("Alpha one").to(f"{_NAV_PATH}?p=1"),
                        NavLink().label("Alpha two").to(f"{_NAV_PATH}?p=2"),
                    ],
                ),
                NavGroup()
                .label("Beta")
                .open()
                .fill(
                    "default",
                    [NavLink().label("Beta one").to(f"{_NAV_PATH}?p=3")],
                ),
            ],
        )
        .fill("footer", [ThemeToggle()])
        .render(_ctx(request))
    )


def nav_page(request: HttpRequest) -> HttpResponse:
    page = request.GET.get("p", "1")
    return _doc(
        request,
        f'<p id="page-marker">page {page}</p>',
        sidebar=_sidebar(request, searchable=True),
        title="nav",
    )


def shell_page(request: HttpRequest) -> HttpResponse:
    return _doc(
        request,
        '<p id="shell-marker">shell</p>'
        '<div style="height:200vh">tall body for scroll-lock checks</div>',
        sidebar=_sidebar(request, searchable=True),
        title="shell",
    )


def toasts_page(request: HttpRequest) -> HttpResponse:
    return render(request, "e2e/toasts.html", {"title": "toasts", "body": "", "sidebar": ""})


def modal_page(request: HttpRequest) -> HttpResponse:
    ui_modal = (
        Modal.make()
        .heading("UI modal")
        .size("sm")
        .body('<p id="ui-modal-body">Are you sure?</p><input id="ui-modal-input">')
        .render(_ctx(request))
    )
    close_btn = (
        '<button type="button" id="close-ui-modal" class="dcc-btn dcc-btn--ghost"'
        " onclick=\"window.dispatchEvent(new CustomEvent('dcc-modal-close'))\">"
        "close via event</button>"
    )
    return _doc(request, close_btn + str(ui_modal), title="modal")


def menu_page(request: HttpRequest) -> HttpResponse:
    menu = (
        Menu.make()
        .label("Actions")
        .icon("ellipsis-vertical")
        .align("end")
        .items(
            [
                mark_safe(
                    '<button type="button" class="dcc-menu__item" id="menu-edit">Edit</button>'
                ),
                mark_safe(
                    '<button type="button" class="dcc-menu__item" id="menu-delete">Delete</button>'
                ),
            ]
        )
        .render(_ctx(request))
    )
    return _doc(request, f'<div style="padding:4rem">{menu}</div>', title="menu")


class _TabForm(forms.Form):
    title = forms.CharField(required=False)
    featured = forms.BooleanField(required=False)


def tabs_page(request: HttpRequest) -> HttpResponse:
    from django_control_components.schemas import Tab, Tabs

    html = (
        Schema.make()
        .form(_TabForm)
        .schema(
            [
                Tabs.make().schema(
                    [
                        Tab.make("Content").schema([TextInput.make("title")]),
                        Tab.make("Settings").schema([Toggle.make("featured")]),
                    ]
                )
            ]
        )
        .render_form(request=request)
    )
    return _doc(request, str(html), title="tabs")


class _VisibilityForm(forms.Form):
    status = forms.ChoiceField(
        choices=[("draft", "Draft"), ("live", "Live"), ("archived", "Archived")],
        required=False,
    )
    slug = forms.CharField(required=False)
    title = forms.CharField(required=True)


def form_page(request: HttpRequest) -> HttpResponse:
    html = (
        Schema.make()
        .form(_VisibilityForm)
        .schema(
            [
                Section.make("Publish").schema(
                    [
                        Select.make("status"),
                        TextInput.make("slug").visible_when("status", equals="live"),
                        TextInput.make("title").required(),
                    ]
                )
            ]
        )
        .render_form(request=request)
    )
    return _doc(request, str(html), title="form")


def table_page(request: HttpRequest) -> HttpResponse:
    from demo.models import Task

    from django_control_components.actions import BulkAction
    from django_control_components.tables import BooleanColumn, Table, TextColumn

    def _noop(records):
        return None

    def build_table(_request):
        return (
            Table.make(Task.objects.all())
            .id("e2e-bulk")
            .columns(
                [
                    TextColumn.make("title").sortable().searchable(),
                    BooleanColumn.make("done"),
                ]
            )
            .client_side()
            .bulk_actions([BulkAction.make("archive").label("Archive").action(_noop)])
            .searchable()
            .set_owner_factory(build_table)
        )

    table = build_table(request).render(request)
    return _doc(request, str(table), title="table")


def blocks_page(request: HttpRequest) -> HttpResponse:
    search = GlobalSearch().endpoint("/e2e/search-api/").render(_ctx(request))
    bell = NotificationBell().endpoint("/e2e/bell-api/").interval(5).render(_ctx(request))
    body = f'<div class="dcc-topbar" style="display:flex;gap:1rem">{search}{bell}</div>'
    return _doc(request, body, title="blocks")


def search_api(request: HttpRequest) -> HttpResponse:
    query = request.GET.get("q", "").strip()
    if not query:
        return HttpResponse("")
    return HttpResponse(
        f'<a class="dcc-globalsearch__result" href="/e2e/nav/?p=9" role="option">'
        f"Result for {query}</a>"
    )


@csrf_exempt
def bell_api(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        return JsonResponse({"unread": 0, "items": []})
    return JsonResponse(
        {
            "unread": 2,
            "items": [
                {"id": 1, "title": "Build passed", "body": "main", "read": False, "level": "info"},
                {"id": 2, "title": "Deploy queued", "read": False, "level": "success"},
            ],
        }
    )


def cotton_tags_page(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "e2e/cotton.html",
        {
            "title": "cotton",
            "sidebar": "",
            "body": "",
            "options": [("draft", "Draft"), ("live", "Live"), ("archived", "Archived")],
            "choices": [("free", "Free"), ("pro", "Pro")],
        },
    )
