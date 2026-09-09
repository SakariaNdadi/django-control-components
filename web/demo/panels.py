from __future__ import annotations

from django.templatetags.static import static

from django_control_components.panels import Panel

from .catalog.registry import PAGES_BEFORE_BLOCKS, PAGES_BLOCKS
from .pages.full_example import FullExamplePage, TaskResource
from .pages.home import HomePage
from .pages.installation import InstallationPage
from .pages.panels_resources import PanelsResourcesPage
from .pages.quickstart import QuickstartPage
from .pages.reference import reference_pages
from .pages.wizards import WizardsPage

docs_panel = (
    Panel("docs")
    .path("")
    .brand("DCC", "cubes", image=static("demo/logo.svg"))
    .resources([TaskResource])
    .pages(
        [
            HomePage,
            InstallationPage,
            QuickstartPage,
            PanelsResourcesPage,
            FullExamplePage,
            *PAGES_BEFORE_BLOCKS,
            WizardsPage,
            *PAGES_BLOCKS,
            *reference_pages(),
        ]
    )
)
