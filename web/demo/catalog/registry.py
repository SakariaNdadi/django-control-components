"""Collects every family module's ``PAGES`` into one organised catalog.

Sorted by family (in ``FAMILY_ORDER``) then title, so the sidebar's
``nav_group`` heading per family - "UI", "Schemas", "Tables", … - stays
contiguous instead of interleaving into one flat alphabetical dump.
"""

from __future__ import annotations

from .examples import actions, blocks, infolists, nav, schemas, tables, ui, widgets
from .page import FAMILY_ORDER, ComponentPageSpec, component_page

_FAMILY_MODULES = (ui, schemas, tables, infolists, widgets, actions, nav, blocks)

ALL_SPECS: list[ComponentPageSpec] = sorted(
    (spec for module in _FAMILY_MODULES for spec in module.PAGES),
    key=lambda spec: (FAMILY_ORDER.index(spec.family), spec.title),
)

CATALOG_PAGES = [component_page(spec) for spec in ALL_SPECS]

#: Split so a hand-written page for a family with no live-render catalog
#: entries (Wizards) can be inserted between them in ``FAMILY_ORDER`` order.
PAGES_BEFORE_BLOCKS = [p for p in CATALOG_PAGES if p.nav_group != "Blocks"]
PAGES_BLOCKS = [p for p in CATALOG_PAGES if p.nav_group == "Blocks"]
