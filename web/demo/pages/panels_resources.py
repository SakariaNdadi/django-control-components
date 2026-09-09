from __future__ import annotations

from ._base import ProsePage


class PanelsResourcesPage(ProsePage):
    template_name = "demo/pages/panels_resources.html"
    slug = "panels-and-resources"
    nav_label = "Panels & Resources"
    nav_icon = "table-columns"
    nav_group = "Getting started"
    page_eyebrow = "Panels"
    page_accent = "#b45309"
    page_title = "Panels, resources & dashboards"
    page_summary = (
        "An admin-independent surface in pure Python. A Panel mounts Resource CRUD "
        "views and DashboardPage metric grids into your URLconf, untouched by "
        "django.contrib.admin."
    )
