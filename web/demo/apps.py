from __future__ import annotations

import datetime
import io

from django.apps import AppConfig
from django.core.files.base import ContentFile
from django.db.models.signals import post_migrate

_PALETTE = {"low": "#0d9488", "medium": "#6366f1", "high": "#dc2626"}


def _cover_png(title: str, priority: str) -> bytes | None:
    """A flat priority-coloured square with the task's initials - just enough
    for the ImageColumn / FileUpload / infolist demos to show a real image."""
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return None
    initials = "".join(word[0] for word in title.split()[:2]).upper()
    img = Image.new("RGB", (240, 240), _PALETTE.get(priority, "#6366f1"))
    draw = ImageDraw.Draw(img)
    draw.text((120, 120), initials, fill="white", anchor="mm")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def _seed_tasks(sender, **kwargs):
    """Fill an empty database with a handful of demo rows so the catalog's
    live Table, Widget and Resource examples have something to render. Runs
    after every migrate; the ``exists()`` guard makes it idempotent and
    keeps it out of the committed migration history."""
    from .models import Task

    if Task.objects.exists():
        return
    today = datetime.date.today()
    rows = [
        ("Ship the release", "high", False, today),
        ("Write the changelog", "medium", True, today - datetime.timedelta(days=2)),
        ("Review open PRs", "medium", False, today + datetime.timedelta(days=1)),
        ("Update dependencies", "low", True, None),
        ("Fix flaky test", "high", False, today + datetime.timedelta(days=3)),
    ]
    for title, priority, done, due in rows:
        task = Task(title=title, priority=priority, done=done, due_date=due)
        png = _cover_png(title, priority)
        if png is not None:
            task.cover.save(f"{title.lower().replace(' ', '-')}.png", ContentFile(png), save=False)
        task.save()


class DemoConfig(AppConfig):
    name = "demo"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self) -> None:
        post_migrate.connect(_seed_tasks, sender=self)
