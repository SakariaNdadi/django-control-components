from __future__ import annotations

from django_control_components.panels import PanelPage


class InstallationPage(PanelPage):
    template_name = "demo/pages/installation.html"
    slug = "installation"
    nav_label = "Installation"
    nav_icon = "download"
    nav_group = "Getting started"

