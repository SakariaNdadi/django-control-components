from __future__ import annotations

from django_control_components.panels import PanelPage


class PanelsResourcesPage(PanelPage):
    template_name = "demo/pages/panels_resources.html"
    slug = "panels-and-resources"
    nav_label = "Panels & Resources"
    nav_icon = "table-columns"
    nav_group = "Getting started"
