"""Declarative catalog pages - the boilerplate-reduction core.

Every one of the ~30+ component pages is authored as a single
``ComponentPageSpec(...)`` literal in ``catalog/examples/*.py``. This module
holds the one factory (``component_page``) that turns such a spec into a
concrete ``PanelPage`` subclass - no per-component view code, no per-component
template.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from django.http import HttpResponse

from django_control_components import htmx
from django_control_components.blocks.base import Block
from django_control_components.core.component import Component
from django_control_components.core.context import RenderContext
from django_control_components.infolists import Infolist
from django_control_components.panels import PanelPage
from django_control_components.panels.widgets import Widget
from django_control_components.schemas import Schema
from django_control_components.tables import Table

from ..blocks import ComponentDemo

if TYPE_CHECKING:
    from collections.abc import Callable

    from django.http import HttpRequest


@dataclass(frozen=True)
class ComponentExample:
    """One runnable snippet for a component page.

    ``code`` is hand-written source text shown verbatim next to the live
    render ``build`` produces - kept in sync by convention (they sit right
    next to each other), not derived from ``build`` via introspection.
    """

    title: str
    code: str
    build: Callable[[HttpRequest], Any]
    note: str = ""


@dataclass(frozen=True)
class ComponentPageSpec:
    """Declarative definition for one component's catalog page."""

    slug: str
    title: str
    family: str
    icon: str = ""
    summary: str = ""
    examples: list[ComponentExample] = field(default_factory=list)
    props_table: list[tuple[str, str, str]] = field(default_factory=list)


#: Sidebar nav-group label per family, and the order families appear in.
#: Sorting the catalog by this order before building pages (see
#: ``catalog/registry.py``) is what makes the sidebar group "Tables", then
#: "Schemas", etc. instead of one flat alphabetical dump.
FAMILY_LABELS: dict[str, str] = {
    "ui": "UI",
    "schemas": "Schemas",
    "tables": "Tables",
    "infolists": "Infolists",
    "widgets": "Widgets",
    "actions": "Actions",
    "wizards": "Wizards",
    "blocks": "Blocks",
}
FAMILY_ORDER: list[str] = list(FAMILY_LABELS)


def _build_demo(
    example: ComponentExample, request: HttpRequest, assets: dict[str, Any]
) -> ComponentDemo:
    """Render whatever ``build`` returned into a ``ComponentDemo``.

    A :class:`Block` (``Card``, ``Row``, ``AppShell``, …) goes into the
    ``preview`` slot so it composes with other blocks. Everything else
    renders itself to HTML up front, since only ``Block``s can be slotted:
    ``Table``/``Schema``/``Infolist`` have their own ``.render(...)``; a
    ``Widget`` collects its CDN assets into ``assets`` (mirroring
    ``DashboardPage``) before rendering; a plain ``Component`` (``Button``,
    ``Badge``, ``Action`` triggers, …) is rendered through a fresh
    ``RenderContext``; a bare string (e.g. ``Action.render_trigger(...)``)
    is used as-is.
    """
    result = example.build(request)
    demo = ComponentDemo(title=example.title, code=example.code, note=example.note)
    if isinstance(result, Block):
        return demo.fill("preview", [result])
    if isinstance(result, (Table, Schema, Infolist)):
        return demo.preview_html(result.render(request=request))
    if isinstance(result, Widget):
        for asset in result.get_assets():
            assets[asset.url] = asset
        return demo.preview_html(result.render(request))
    if isinstance(result, Component):
        return demo.preview_html(result.render(RenderContext(request=request)))
    return demo.preview_html(result)


def component_page(spec: ComponentPageSpec) -> type[PanelPage]:
    """Turn a ``ComponentPageSpec`` into a mountable ``PanelPage`` subclass."""

    class _Page(PanelPage):
        template_name = "demo/catalog/component_page.html"
        slug = spec.slug
        nav_label = spec.title
        nav_icon = spec.icon
        nav_group = FAMILY_LABELS.get(spec.family, spec.family.title())

        def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Any:
            # Mirrors TableMixin.get(): a Table answers its own sort/filter/
            # search/pagination htmx requests by re-rendering just its content
            # fragment - without this, the catalog page would re-render the
            # *whole* page and swap that into the table's fragment target, so
            # every interactive control on every Table demo would silently
            # no-op. Several examples on one page may each hold a Table, so
            # find the one whose id matches the request.
            table_id = request.GET.get("_dcc_table")
            if htmx.is_htmx(request) and table_id:
                for example in spec.examples:
                    result = example.build(request)
                    if isinstance(result, Table) and result.table_id == table_id:
                        return HttpResponse(result.render_content(request))
            return super().get(request, *args, **kwargs)

        def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            ctx = super().get_context_data(**kwargs)
            ctx["spec"] = spec
            assets: dict[str, Any] = {}
            ctx["demos"] = [_build_demo(example, self.request, assets) for example in spec.examples]
            ctx["widget_assets"] = list(assets.values())
            return ctx

    _Page.__name__ = f"{spec.title.replace(' ', '')}Page"
    _Page.__qualname__ = _Page.__name__
    return _Page
