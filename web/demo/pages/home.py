from __future__ import annotations

from ._base import ProsePage


class HomePage(ProsePage):
    template_name = "demo/pages/home.html"
    slug = ""
    nav_label = "Home"
    nav_icon = "house"
    nav_group = "Overview"
    page_header = False  # the home page carries its own hero
