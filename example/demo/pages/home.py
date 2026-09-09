from __future__ import annotations

from django_control_components.panels import PanelPage


class HomePage(PanelPage):
    template_name = "demo/pages/home.html"
    slug = ""
    nav_label = "Home"
    nav_icon = "house"
    nav_group = "Overview"
