"""Navigation blocks - the pieces a sidebar or nav column is built from.

``NavLink`` / ``NavGroup`` (collapsible) / ``NavHeading`` / ``NavDivider`` /
``NavAction`` / ``NavUser`` / ``ThemeToggle`` compose inside a :class:`Sidebar`
(``blocks/chrome.py``). Collapse state is an Alpine component (``dccNav``) that
persists to ``localStorage``; the panel's ``_nav.html`` renders its stored
navigation tree through these same blocks.
"""

from __future__ import annotations

import hashlib
from typing import TYPE_CHECKING, Any, Self

from django.urls import NoReverseMatch, reverse

from ..core.component import setter
from ..icons import render_icon
from .base import Block

if TYPE_CHECKING:
    from ..core.context import RenderContext

_T = "django_control_components/blocks/"


def _resolve_url(value: str) -> tuple[str, bool]:
    """``(url, is_external)``. A value that looks like a path/anchor/URL is used
    verbatim; anything else is treated as a URL name and reversed (a miss →
    ``""``, never an exception)."""
    if not value:
        return "", False
    if value.startswith(("/", "#", "?", "http://", "https://", "mailto:")):
        return value, value.startswith(("http://", "https://", "mailto:"))
    try:
        return reverse(value), False
    except NoReverseMatch:
        return "", False


def _group_id(text: str) -> str:
    return "navg-" + hashlib.md5(text.encode("utf-8")).hexdigest()[:8]  # noqa: S324


def _request_path(ctx: RenderContext) -> str:
    return getattr(getattr(ctx, "request", None), "path", "") or ""


class NavLink(Block):
    """One navigation entry - an ``<a>`` with an optional icon, count badge and
    colour dot."""

    slots = ()
    template_name = _T + "nav_link.html"

    @setter
    def label(self, value: Any) -> Self:
        return self._set("label", value)

    @setter
    def icon(self, value: str) -> Self:
        return self._set("icon", value)

    @setter
    def image(self, value: str) -> Self:
        """A logo / avatar URL shown in place of the icon."""
        return self._set("image", value)

    @setter
    def image_alt(self, value: str) -> Self:
        return self._set("image_alt", value)

    @setter
    def to(self, value: str) -> Self:
        """A URL path, an anchor, or a URL name."""
        return self._set("to", value)

    @setter
    def badge(self, value: Any) -> Self:
        return self._set("badge", value)

    @setter
    def dot(self, value: str) -> Self:
        """A CSS colour for a leading square (project-swatch style)."""
        return self._set("dot", value)

    @setter
    def external(self, value: bool = True) -> Self:
        return self._set("external", value)

    @setter
    def active(self, value: bool) -> Self:
        """Force the active state (the panel passes its own computed value)."""
        return self._set("active", value)

    def active_for(self, prefix: str) -> Self:
        """Mark active when ``request.path`` starts with ``prefix``. Plain
        method - not a kwarg."""
        return self._set("active_for", prefix)

    def get_view_data(self, ctx: RenderContext) -> dict[str, Any]:
        data = super().get_view_data(ctx)
        url, ext = _resolve_url(str(self.resolve("to", ctx, "") or ""))
        external = bool(self._config.get("external")) or ext
        data["url"] = url
        data["external"] = external
        data["label"] = self.resolve("label", ctx, "")
        data["icon_html"] = render_icon(self._config.get("icon"))
        data["image"] = self._config.get("image", "")
        data["image_alt"] = self._config.get("image_alt", "")
        badge = self.resolve("badge", ctx, "")
        data["badge"] = "" if badge in (None, "") else str(badge)
        data["dot"] = self._config.get("dot", "")
        if "active" in self._config:
            data["active"] = bool(self._config["active"])
        else:
            prefix = self._config.get("active_for") or url
            data["active"] = bool(prefix) and not external and _request_path(ctx).startswith(prefix)
        return data


class NavAction(NavLink):
    """A muted call-to-action row - ``+ Add new project``."""

    template_name = _T + "nav_action.html"


class NavGroup(Block):
    """A collapsible section. Its ``<button>`` toggles the child list;
    ``dccNav`` persists the open/closed state."""

    slots = ("default",)
    template_name = _T + "nav_group.html"

    @setter
    def label(self, value: Any) -> Self:
        return self._set("label", value)

    @setter
    def icon(self, value: str) -> Self:
        return self._set("icon", value)

    @setter
    def image(self, value: str) -> Self:
        """A logo URL shown in place of the icon."""
        return self._set("image", value)

    @setter
    def image_alt(self, value: str) -> Self:
        return self._set("image_alt", value)

    @setter
    def id(self, value: str) -> Self:
        return self._set("id", value)

    @setter
    def open(self, value: bool = True) -> Self:
        """Start expanded (unless the viewer already toggled it)."""
        return self._set("open", value)

    def get_view_data(self, ctx: RenderContext) -> dict[str, Any]:
        data = super().get_view_data(ctx)
        label = str(self.resolve("label", ctx, "") or "")
        data["label"] = label
        data["icon_html"] = render_icon(self._config.get("icon"))
        data["image"] = self._config.get("image", "")
        data["image_alt"] = self._config.get("image_alt", "")
        data["group_id"] = self._config.get("id") or _group_id(label)
        data["default_open"] = bool(self._config.get("open"))
        return data


class NavHeading(Block):
    """A non-interactive section label."""

    slots = ()
    template_name = _T + "nav_heading.html"

    @setter
    def label(self, value: Any) -> Self:
        return self._set("label", value)

    def get_view_data(self, ctx: RenderContext) -> dict[str, Any]:
        data = super().get_view_data(ctx)
        data["label"] = self.resolve("label", ctx, "")
        return data


class NavDivider(Block):
    """A horizontal rule between nav sections."""

    slots = ()
    template_name = _T + "nav_divider.html"


class NavUser(Block):
    """An account card pinned in the sidebar footer, with an optional menu."""

    slots = ()
    template_name = _T + "nav_user.html"

    @setter
    def label(self, value: Any) -> Self:
        """The display name (``name`` is the :class:`Component` identity property,
        so the display name uses ``label``)."""
        return self._set("label", value)

    @setter
    def email(self, value: Any) -> Self:
        return self._set("email", value)

    @setter
    def avatar(self, value: str) -> Self:
        return self._set("avatar", value)

    @setter
    def menu(self, items: list[tuple[str, str]]) -> Self:
        """``[(label, url_or_name), ...]``."""
        return self._set("menu", list(items))

    def get_view_data(self, ctx: RenderContext) -> dict[str, Any]:
        data = super().get_view_data(ctx)
        data["label"] = self.resolve("label", ctx, "")
        data["email"] = self.resolve("email", ctx, "")
        data["avatar"] = self._config.get("avatar", "")
        data["menu"] = [
            {"label": label, "url": _resolve_url(str(target))[0]}
            for label, target in (self._config.get("menu") or [])
        ]
        return data


class ThemeToggle(Block):
    """The light / dark / auto cycle button. Renders inside a ``dccShell``
    scope (``AppShell`` / the panel shell provide it)."""

    slots = ()
    template_name = _T + "nav_theme_toggle.html"
