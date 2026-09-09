from __future__ import annotations

from ._base import ProsePage


class QuickstartPage(ProsePage):
    template_name = "demo/pages/quickstart.html"
    slug = "quickstart"
    nav_label = "Quickstart"
    nav_icon = "bolt"
    nav_group = "Getting started"
    page_eyebrow = "Schemas"
    page_accent = "#0891b2"
    page_title = "Quickstart"
    page_summary = (
        "Build responsive form layouts in Python that decorate a standard Django Form / ModelForm."
    )
