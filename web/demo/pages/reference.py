"""The written docs (``docs/*.md``), rendered into the demo site.

One :class:`~django_control_components.panels.PanelPage` per markdown file, so
every reference page in ``docs/`` shows up in the sidebar under "Reference"
instead of only being readable on GitHub. The markdown is the single source -
this module never copies prose, it renders the file at request time (cached on
mtime, so an edit under ``runserver`` shows up on the next reload).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import markdown
from django.conf import settings

from django_control_components.blocks import PageShell, Prose
from django_control_components.panels import PanelPage

_DOCS_DIR = Path(settings.BASE_DIR).parent / "docs"
_GITHUB_BLOB = "https://github.com/SakariaNdadi/django-control-components/blob/master/"

#: ``stem`` -> ``(nav_label, icon)``, in sidebar order. ``README`` is handled
#: separately as the section landing page. A file in ``docs/`` not listed here
#: is still reachable by URL but gets no sidebar entry.
_PAGES: list[tuple[str, str, str]] = [
    ("architecture", "Architecture", "sitemap"),
    ("settings", "Settings & install", "gear"),
    ("permissions", "Permissions", "shield-halved"),
    ("integration", "Existing projects", "puzzle-piece"),
    ("navigation", "Navigation", "bars"),
    ("panels", "Panels & Resources", "table-columns"),
    ("schemas", "Schemas", "list-check"),
    ("tables", "Tables", "table"),
    ("actions", "Actions", "bolt"),
    ("infolists", "Infolists", "rectangle-list"),
    ("widgets", "Widgets", "chart-simple"),
    ("wizards", "Wizards", "diagram-project"),
    ("ui", "UI primitives", "shapes"),
    ("blocks", "Blocks", "cubes"),
    ("images", "Images", "image"),
    ("views-and-mixins", "Views & mixins", "code"),
    ("callbacks", "Callbacks", "link"),
    ("errors", "Errors", "triangle-exclamation"),
    ("studio", "Studio", "wand-magic-sparkles"),
    ("no-code", "Studio spec format", "file-code"),
    ("testing", "Testing", "vial"),
    ("deployment", "Deployment", "rocket"),
]

_LINK = re.compile(r"(?<=\]\()([^)]+)(?=\))")
#: stem -> (mtime, title, summary, body_html)
_RENDER_CACHE: dict[str, tuple[float, str, str, str]] = {}

_MD = markdown.Markdown(
    extensions=["fenced_code", "tables", "toc", "sane_lists", "attr_list"],
    output_format="html",
)


def _rewrite_link(target: str) -> str:
    """A relative ``*.md`` link in a doc points at a sibling doc; here it has to
    point at ``/reference/<stem>/``. Everything else is left alone."""
    if target.startswith(("http://", "https://", "#", "mailto:", "/")):
        return target
    if target.startswith("../"):
        return _GITHUB_BLOB + target[3:]
    path, _, anchor = target.partition("#")
    anchor = f"#{anchor}" if anchor else ""
    if "/" in path or not path.endswith(".md"):
        return target
    stem = path[: -len(".md")]
    if stem == "README":
        return f"/reference/{anchor}"
    return f"/reference/{stem}/{anchor}"


def _render(stem: str) -> tuple[str, str, str]:
    """Return ``(title, summary, body_html)`` for ``docs/<stem>.md``, cached on
    file mtime."""
    source_path = _DOCS_DIR / f"{stem}.md"
    mtime = source_path.stat().st_mtime
    cached = _RENDER_CACHE.get(stem)
    if cached is not None and cached[0] == mtime:
        return cached[1], cached[2], cached[3]

    raw = source_path.read_text(encoding="utf-8")
    raw = _LINK.sub(lambda m: _rewrite_link(m.group(0)), raw)

    # The H1 becomes the PageShell title; drop it from the prose so it is not
    # rendered twice.
    title, body = "Reference", raw
    lines = raw.splitlines()
    if lines and lines[0].startswith("# "):
        title = lines[0][2:].strip()
        body = "\n".join(lines[1:]).lstrip()
    first_para = body.split("\n\n", 1)[0] if body else ""
    summary = (
        ""
        if first_para[:1] in {"|", "#", "-", "*", "`", ">"}
        else " ".join(first_para.split())[:200]
    )

    _MD.reset()
    html = _MD.convert(body)
    _RENDER_CACHE[stem] = (mtime, title, summary, html)
    return title, summary, html


_ACCENT = "#0f766e"


def reference_page(
    stem: str, *, nav_label: str = "", nav_icon: str = "", slug: str = ""
) -> type[PanelPage]:
    """Build a mountable ``PanelPage`` that renders ``docs/<stem>.md``."""

    class _DocPage(PanelPage):
        template_name = "demo/pages/_shell.html"

        def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            ctx = super().get_context_data(**kwargs)
            title, summary, html = _render(stem)
            ctx["page_block"] = (
                PageShell()
                .eyebrow("Reference")
                .title(title)
                .summary(summary)
                .accent(_ACCENT)
                .fill("content", [Prose().html(html)])
            )
            ctx["widget_assets"] = []
            return ctx

    _DocPage.slug = slug or f"reference/{stem}"
    _DocPage.nav_label = nav_label
    _DocPage.nav_icon = nav_icon
    _DocPage.nav_group = "Reference" if nav_label else ""
    _DocPage.__name__ = f"Doc{stem.title().replace('-', '')}Page"
    _DocPage.__qualname__ = _DocPage.__name__
    return _DocPage


def reference_pages() -> list[type[PanelPage]]:
    """Every doc page, landing page first."""
    pages: list[type[PanelPage]] = [
        reference_page("README", nav_label="Reference", nav_icon="book", slug="reference")
    ]
    pages += [reference_page(stem, nav_label=label, nav_icon=icon) for stem, label, icon in _PAGES]
    return pages
