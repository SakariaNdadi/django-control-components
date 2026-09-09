from __future__ import annotations

from django_control_components.panels import PanelPage
from .wizard_demo import LiveWizardDemoView


class WizardsPage(PanelPage):
    template_name = "demo/pages/wizards.html"
    slug = "wizards"
    nav_label = "Wizard View"
    nav_icon = "list-ol"
    nav_group = "Wizards"

    def get(self, request, *args, **kwargs):
        wizard_view = LiveWizardDemoView.as_view()
        response = wizard_view(request, *args, **kwargs)
        if hasattr(response, "render"):
            response.render()
        
        context = self.get_context_data(**kwargs)
        context["live_wizard_html"] = response.content.decode("utf-8")
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        wizard_view = LiveWizardDemoView.as_view()
        return wizard_view(request, *args, **kwargs)

