"""Page-level blocks - the frame a demo/docs page (or any content page) sits in.

``PageShell`` renders a title header (an eyebrow pill + ``<h1>`` + summary) above
a ``content`` slot. ``Prose`` wraps a run of authored HTML.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

from ..core.component import setter
from .base import Block

if TYPE_CHECKING:
    from ..core.context import RenderContext


class PageShell(Block):
    """A page: a generated header (unless the ``header`` slot is filled) over a
    ``content`` slot."""

    slots = ("header", "content")
    template_name = "django_control_components/blocks/page_shell.html"

    @setter
    def title(self, value: Any) -> Self:
        return self._set("title", value)

    @setter
    def eyebrow(self, value: Any) -> Self:
        """A short label above the title (a family / section tag)."""
        return self._set("eyebrow", value)

    @setter
    def summary(self, value: Any) -> Self:
        return self._set("summary", value)

    @setter
    def accent(self, value: str) -> Self:
        """A CSS colour for the eyebrow / header rule (``--dcc-page-accent``)."""
        return self._set("accent", value)

    def get_view_data(self, ctx: RenderContext) -> dict[str, Any]:
        data = super().get_view_data(ctx)
        data["title"] = self.resolve("title", ctx, "")
        data["eyebrow"] = self.resolve("eyebrow", ctx, "")
        data["summary"] = self.resolve("summary", ctx, "")
        data["accent"] = self._config.get("accent", "")
        data["has_header"] = bool(self._slots.get("header"))
        data["has_content"] = bool(self._slots.get("content"))
        return data


class Prose(Block):
    """A block of authored rich text. ``.html(...)`` is code-only - a stored
    studio spec cannot set it (``CODE_ONLY_SETTERS``)."""

    slots = ()
    template_name = "django_control_components/blocks/prose.html"

    @setter
    def html(self, value: str) -> Self:
        return self._set("html", value)

    def get_view_data(self, ctx: RenderContext) -> dict[str, Any]:
        data = super().get_view_data(ctx)
        data["html"] = str(self.resolve("html", ctx, "") or "")
        return data
