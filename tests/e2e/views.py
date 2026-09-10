"""A minimal panel page for browser tests.

Two open nav groups plus a sidebar link back to this same view, so a test can
collapse a group, trigger a full-page navigation, and check the group's toggle
still works on the freshly rendered page.
"""

from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from django_control_components.blocks import NavGroup, NavLink, Sidebar
from django_control_components.core.context import RenderContext

_PATH = "/e2e/nav/"


def nav_page(request: HttpRequest) -> HttpResponse:
    page = request.GET.get("p", "1")
    sidebar = (
        Sidebar()
        .brand("E2E")
        .fill(
            "default",
            [
                NavGroup()
                .label("Alpha")
                .open()
                .fill(
                    "default",
                    [
                        NavLink().label("Alpha one").to(f"{_PATH}?p=1"),
                        NavLink().label("Alpha two").to(f"{_PATH}?p=2"),
                    ],
                ),
                NavGroup()
                .label("Beta")
                .open()
                .fill(
                    "default",
                    [NavLink().label("Beta one").to(f"{_PATH}?p=3")],
                ),
            ],
        )
        .render(RenderContext(request=request))
    )
    return render(request, "e2e_nav.html", {"sidebar": sidebar, "page": page})
