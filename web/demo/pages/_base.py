from __future__ import annotations

from typing import Any

from django_control_components.blocks import PageShell
from django_control_components.panels import PanelPage


class ProsePage(PanelPage):
    """A demo page whose frame is a :class:`PageShell` block and whose body is
    authored HTML in a ``{% block prose %}`` (``demo/pages/_prose.html``)."""

    template_name = "demo/pages/_prose.html"
    page_header: bool = True
    page_eyebrow: str = ""
    page_title: str = ""
    page_summary: str = ""
    page_accent: str = "#4f46e5"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        if self.page_header:
            ctx["page_block"] = (
                PageShell()
                .eyebrow(self.page_eyebrow)
                .title(self.page_title or self.nav_label)
                .summary(self.page_summary)
                .accent(self.page_accent)
            )
        return ctx
