from __future__ import annotations

from ._base import ProsePage
from .wizard_demo import LiveWizardDemoView


class WizardsPage(ProsePage):
    slug = "wizards"
    nav_label = "Wizard View"
    nav_icon = "list-ol"
    nav_group = "Wizards"
    page_eyebrow = "Wizards"
    page_accent = "#0d9488"
    page_title = "Wizard views"
    page_summary = (
        "Multi-step forms on django-formtools, with htmx step swapping, per-step "
        "Django validation, and a review infolist."
    )

    def get(self, request, *args, **kwargs):
        view = LiveWizardDemoView.as_view()
        response = view(request, *args, **kwargs)
        if hasattr(response, "render"):
            response.render()
        context = self.get_context_data(**kwargs)
        context["live_wizard_html"] = response.content.decode("utf-8")
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        return LiveWizardDemoView.as_view()(request, *args, **kwargs)
