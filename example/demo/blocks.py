"""``ComponentDemo`` - a code+preview split card for the catalog pages.

Project-local docs infrastructure, built the way any host app builds a custom
block: subclass :class:`Block`, add a template. Not part of
``django_control_components`` itself.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

from django_control_components.blocks.base import Block
from django_control_components.core.component import setter

if TYPE_CHECKING:
    from django_control_components.core.context import RenderContext


class ComponentDemo(Block):
    """One runnable example: a title, an optional note, a live preview and
    its source code side by side. The preview is either a live ``Block`` /
    ``Component`` filled into the ``preview`` slot, or - for ``Table`` /
    ``Schema`` / ``Infolist`` (which render themselves, not through
    ``Component``) - pre-rendered HTML passed to ``.preview_html(...)``."""

    slots = ("preview",)
    template_name = "demo/blocks/component_demo.html"

    @setter
    def title(self, value: str) -> Self:
        return self._set("title", value)

    @setter
    def code(self, value: str) -> Self:
        return self._set("code", value)

    @setter
    def note(self, value: str) -> Self:
        return self._set("note", value)

    @setter
    def preview_html(self, value: Any) -> Self:
        return self._set("preview_html", value)

    def get_view_data(self, ctx: RenderContext) -> dict[str, Any]:
        data = super().get_view_data(ctx)
        data["title"] = self._config.get("title", "")
        data["code"] = self._config.get("code", "")
        data["note"] = self._config.get("note", "")
        data["preview_html"] = self._config.get("preview_html", "")
        return data


class Html(Block):
    """A leaf block wrapping raw HTML - lets a layout-block demo (Row, Grid,
    Card, …) hold visible filler content instead of an empty slot. A
    downstream project registers a custom block exactly this way; not part
    of ``django_control_components`` itself."""

    template_name = "demo/blocks/html.html"

    @setter
    def content(self, value: str) -> Self:
        return self._set("content", value)

    def get_view_data(self, ctx: RenderContext) -> dict[str, Any]:
        data = super().get_view_data(ctx)
        data["content"] = self._config.get("content", "")
        return data
