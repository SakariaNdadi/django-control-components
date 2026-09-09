"""Page/layout building blocks - sixth ``TypeRegistry``, alongside
``FIELD_TYPES`` / ``COLUMN_TYPES`` / ``FILTER_TYPES`` / ``ENTRY_TYPES`` /
``WIDGET_TYPES``. A type registered here reaches the studio palette for free
through ``studio/palette.py`` and inherits ``strip_privileged_setters``.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from ..core.type_registry import TypeRegistry
from .base import Block
from .chrome import AppShell, Footer, GlobalSearch, Navbar, NotificationBell, Sidebar
from .layout import Card, Column, Divider, Grid, Row, Spacer, Stack
from .nav import (
    NavAction,
    NavDivider,
    NavGroup,
    NavHeading,
    NavLink,
    NavUser,
    ThemeToggle,
)
from .page import PageShell, Prose

BLOCK_TYPES: TypeRegistry[Block] = TypeRegistry("block")

for _cls, _label, _icon, _cat, _slots in (
    (Stack, "Stack", "bars-staggered", "block", ("default",)),
    (Row, "Row", "grip-lines-vertical", "block", ("default",)),
    (Grid, "Grid", "table-cells", "block", ("default",)),
    (Column, "Column", "table-columns", "block", ("default",)),
    (Card, "Card", "square", "block", ("header", "body", "footer")),
    (Divider, "Divider", "minus", "block", ()),
    (Spacer, "Spacer", "up-down", "block", ()),
    (PageShell, "Page shell", "window-maximize", "block", ("header", "content")),
    (Prose, "Prose", "align-left", "block", ()),
    (AppShell, "App shell", "window-maximize", "block", ("topbar", "sidebar", "content", "footer")),
    (Navbar, "Navbar", "window-minimize", "block", ("start", "end")),
    (Sidebar, "Sidebar", "table-columns", "block", ("default", "footer")),
    (Footer, "Footer", "window-minimize", "block", ("default",)),
    (NotificationBell, "Notification bell", "bell", "block", ()),
    (GlobalSearch, "Global search", "magnifying-glass", "block", ()),
    (NavLink, "Nav link", "link", "nav", ()),
    (NavGroup, "Nav group", "folder-tree", "nav", ("default",)),
    (NavHeading, "Nav heading", "heading", "nav", ()),
    (NavDivider, "Nav divider", "minus", "nav", ()),
    (NavAction, "Nav action", "plus", "nav", ()),
    (NavUser, "Nav user", "user", "nav", ()),
    (ThemeToggle, "Theme toggle", "circle-half-stroke", "nav", ()),
):
    BLOCK_TYPES.register(
        _cls,
        label=_label,
        icon=_icon,
        category=_cat,
        accepts_children=bool(_slots),
        # belt and braces: ``html`` is already in CODE_ONLY_SETTERS, but the
        # name denylist is not the boundary a raw-HTML sink should rely on.
        setters={"html": {"requires": "superuser"}} if _cls is Prose else None,
    )


def block(
    label: str | None = None,
    *,
    name: str | None = None,
    icon: str = "",
    category: str = "block",
    setters: dict[str, dict[str, Any]] | None = None,
) -> Callable[[type[Block]], type[Block]]:
    """Class decorator: register a custom :class:`Block` so it is draggable in
    the studio palette immediately - the sugar form of ``BLOCK_TYPES.register``.

        @block("Callout", icon="bullhorn")
        class Callout(Block):
            slots = ("default",)
            template_name = "myapp/blocks/callout.html"

    If the block's template renders a value through ``|safe``, gate that setter
    so a stored spec cannot reach it::

        @block("Embed", setters={"content": {"requires": "superuser"}})

    ``CODE_ONLY_SETTERS`` only knows the *names* the library ships; a custom
    raw-HTML setter under any other name is otherwise spec-writable.
    """

    def decorate(cls: type[Block]) -> type[Block]:
        BLOCK_TYPES.register(
            cls,
            name=name,
            label=label,
            icon=icon,
            category=category,
            accepts_children=bool(getattr(cls, "slots", ())),
            setters=setters,
        )
        return cls

    return decorate


__all__ = [
    "BLOCK_TYPES",
    "AppShell",
    "Block",
    "Card",
    "Column",
    "Divider",
    "Footer",
    "GlobalSearch",
    "Grid",
    "NavAction",
    "NavDivider",
    "NavGroup",
    "NavHeading",
    "NavLink",
    "NavUser",
    "Navbar",
    "NotificationBell",
    "PageShell",
    "Prose",
    "Row",
    "Sidebar",
    "Spacer",
    "Stack",
    "ThemeToggle",
    "block",
]
