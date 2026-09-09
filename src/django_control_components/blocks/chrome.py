"""Chrome blocks - the page frame a studio-built app sits in.

``AppShell`` is the root: a header, a sidebar, the content, a footer. It reuses
the existing ``.dcc-panel`` structure and the ``dccShell()`` Alpine component
(nav drawer + persisted 3-state theme) so a shell built here renders the same
markup as the hand-coded ``panels/base.html``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

from ..core.component import setter
from .base import Block

if TYPE_CHECKING:
    from ..core.context import RenderContext


class AppShell(Block):
    """Root page frame: ``topbar`` / ``sidebar`` / ``content`` / ``footer``."""

    slots = ("topbar", "sidebar", "content", "footer")
    template_name = "django_control_components/blocks/app_shell.html"

    @setter
    def sidebar_width(self, value: str) -> Self:
        return self._set("sidebar_width", value)

    def get_view_data(self, ctx: RenderContext) -> dict[str, Any]:
        data = super().get_view_data(ctx)
        data["sidebar_width"] = self._config.get("sidebar_width", "15rem")
        data["has_sidebar"] = bool(self._slots.get("sidebar"))
        data["has_topbar"] = bool(self._slots.get("topbar"))
        data["has_footer"] = bool(self._slots.get("footer"))
        return data


class Navbar(Block):
    """A horizontal bar with a leading and a trailing region."""

    slots = ("start", "end")
    template_name = "django_control_components/blocks/navbar.html"

    @setter
    def brand(self, value: str) -> Self:
        return self._set("brand", value)

    def get_view_data(self, ctx: RenderContext) -> dict[str, Any]:
        data = super().get_view_data(ctx)
        data["brand"] = self._config.get("brand", "")
        return data


class Sidebar(Block):
    """A vertical nav column. ``default`` holds the scrolling nav list (nav
    blocks - ``NavLink`` / ``NavGroup`` / ``NavHeading`` / ``NavDivider`` /
    ``NavAction``); ``footer`` is pinned to the bottom (a ``ThemeToggle``, a
    ``NavUser`` card, help links)."""

    slots = ("default", "footer")
    template_name = "django_control_components/blocks/sidebar.html"

    @setter
    def brand(self, value: str) -> Self:
        return self._set("brand", value)

    @setter
    def brand_icon(self, value: str) -> Self:
        return self._set("brand_icon", value)

    @setter
    def brand_image(self, value: str) -> Self:
        """A logo image URL shown in place of ``brand_icon``."""
        return self._set("brand_image", value)

    @setter
    def brand_image_alt(self, value: str) -> Self:
        return self._set("brand_image_alt", value)

    @setter
    def brand_url(self, value: str) -> Self:
        """A URL path or URL name - the brand becomes a link."""
        return self._set("brand_url", value)

    @setter
    def searchable(self, value: bool = True) -> Self:
        return self._set("searchable", value)

    def get_view_data(self, ctx: RenderContext) -> dict[str, Any]:
        from django.urls import NoReverseMatch, reverse

        data = super().get_view_data(ctx)
        data["brand"] = self._config.get("brand", "")
        data["brand_icon"] = self._config.get("brand_icon", "")
        data["brand_image"] = self._config.get("brand_image", "")
        data["brand_image_alt"] = self._config.get("brand_image_alt", "")
        data["searchable"] = self._config.get("searchable", False)
        raw = str(self._config.get("brand_url", "") or "")
        if raw and not raw.startswith(("/", "#", "http://", "https://")):
            try:
                raw = reverse(raw)
            except NoReverseMatch:
                raw = ""
        data["brand_url"] = raw
        return data


class Footer(Block):
    """A page footer."""

    slots = ("default",)
    template_name = "django_control_components/blocks/footer.html"


class NotificationBell(Block):
    """A bell that polls an endpoint for the unread count and shows recent
    notifications. ``endpoint`` defaults to ``dcc_studio:notifications`` when
    that URL is mounted; a project can point it elsewhere. No websockets."""

    slots = ()
    template_name = "django_control_components/blocks/notification_bell.html"

    @setter
    def endpoint(self, value: str) -> Self:
        return self._set("endpoint", value)

    @setter
    def interval(self, value: int) -> Self:
        return self._set("interval", int(value))

    def get_view_data(self, ctx: RenderContext) -> dict[str, Any]:
        from django.urls import NoReverseMatch, reverse

        data = super().get_view_data(ctx)
        endpoint = self._config.get("endpoint")
        if not endpoint:
            try:
                endpoint = reverse("dcc_studio:notifications")
            except NoReverseMatch:
                endpoint = ""
        data["endpoint"] = endpoint
        data["interval"] = int(self._config.get("interval", 30))
        return data


class GlobalSearch(Block):
    """A top-bar search input. On input it ``GET``s ``endpoint`` with ``?q=``
    and drops the returned HTML fragment into a results panel - the endpoint
    owns escaping, the same contract as any htmx partial. Rendered by a panel
    when ``Panel.global_search_url(...)`` is set."""

    slots = ()
    template_name = "django_control_components/blocks/global_search.html"

    @setter
    def endpoint(self, value: str) -> Self:
        """A URL path or URL name that returns an HTML results fragment."""
        return self._set("endpoint", value)

    def get_view_data(self, ctx: RenderContext) -> dict[str, Any]:
        from django.urls import NoReverseMatch, reverse

        data = super().get_view_data(ctx)
        raw = str(self._config.get("endpoint", "") or "")
        if raw and not raw.startswith(("/", "http://", "https://")):
            try:
                raw = reverse(raw)
            except NoReverseMatch:
                raw = ""
        data["endpoint"] = raw
        return data
