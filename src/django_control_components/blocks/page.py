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

_EDGES = ("top", "right", "bottom", "left")
_ALLOWED = set("0123456789.-% abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ()")


def _clean_len(value: Any) -> str:
    """A CSS length, stripped to a safe character set (digits, units, ``calc()``)."""
    text = str(value).strip()
    return text if text and all(char in _ALLOWED for char in text) else ""


def _box_style(prefix: str, box: dict[str, Any]) -> str:
    parts = []
    for edge in _EDGES:
        length = _clean_len(box[edge]) if box.get(edge) is not None else ""
        if length:
            parts.append(f"{prefix}-{edge}:{length}")
    return ";".join(parts)


def _resolve_box(value: Any, top: Any, right: Any, bottom: Any, left: Any) -> dict[str, Any]:
    box = dict.fromkeys(_EDGES, value)
    for edge, override in zip(_EDGES, (top, right, bottom, left), strict=True):
        if override is not None:
            box[edge] = override
    return box


def spacing_style(padding: Any = None, margin: Any = None) -> str:
    """A sanitised ``padding-*`` / ``margin-*`` inline-style string. ``padding`` /
    ``margin`` is a CSS length (all four edges) or an edge->length dict. Shared by
    :class:`PageShell` and ``Panel.content_spacing``."""

    def _box(spec: Any) -> dict[str, Any]:
        return spec if isinstance(spec, dict) else dict.fromkeys(_EDGES, spec)

    parts = []
    if padding is not None:
        parts.append(_box_style("padding", _box(padding)))
    if margin is not None:
        parts.append(_box_style("margin", _box(margin)))
    return ";".join(part for part in parts if part)


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

    def padding(
        self,
        value: Any = None,
        *,
        top: Any = None,
        right: Any = None,
        bottom: Any = None,
        left: Any = None,
    ) -> Self:
        """Inner spacing on the page wrapper. ``value`` sets all four edges; the
        keyword args override individual edges. Each is a CSS length
        (``"2rem"``, ``"clamp(1rem,4vw,3rem)"``)."""
        return self._set("padding", _resolve_box(value, top, right, bottom, left))

    def margin(
        self,
        value: Any = None,
        *,
        top: Any = None,
        right: Any = None,
        bottom: Any = None,
        left: Any = None,
    ) -> Self:
        """Outer spacing on the page wrapper. Same call shape as :meth:`padding`."""
        return self._set("margin", _resolve_box(value, top, right, bottom, left))

    def get_view_data(self, ctx: RenderContext) -> dict[str, Any]:
        data = super().get_view_data(ctx)
        data["title"] = self.resolve("title", ctx, "")
        data["eyebrow"] = self.resolve("eyebrow", ctx, "")
        data["summary"] = self.resolve("summary", ctx, "")
        data["accent"] = self._config.get("accent", "")
        data["style"] = spacing_style(
            self._config.get("padding"), self._config.get("margin")
        )
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
