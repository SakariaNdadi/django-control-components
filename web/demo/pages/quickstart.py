from __future__ import annotations

from django_control_components.panels import PanelPage


class QuickstartPage(PanelPage):
    template_name = "demo/pages/quickstart.html"
    slug = "quickstart"
    nav_label = "Quickstart"
    nav_icon = "bolt"
    nav_group = "Getting started"
