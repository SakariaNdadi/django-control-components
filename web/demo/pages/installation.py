from __future__ import annotations

from ._base import ProsePage


class InstallationPage(ProsePage):
    slug = "installation"
    nav_label = "Installation"
    nav_icon = "download"
    nav_group = "Getting started"
    page_eyebrow = "Getting started"
    page_title = "Installation & setup"
    page_summary = (
        "Filament-inspired schema, table and action builders for Django - declare "
        "UI in Python, rendered through django-cotton, wired to real django.forms."
    )
