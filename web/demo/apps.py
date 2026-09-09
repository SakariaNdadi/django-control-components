from __future__ import annotations

import datetime

from django.apps import AppConfig
from django.db.models.signals import post_migrate


def _seed_tasks(sender, **kwargs):
    """Fill an empty database with a handful of demo rows so the catalog's
    live Table, Widget and Resource examples have something to render. Runs
    after every migrate; the ``exists()`` guard makes it idempotent and
    keeps it out of the committed migration history."""
    from .models import Task

    if Task.objects.exists():
        return
    today = datetime.date.today()
    Task.objects.bulk_create(
        [
            Task(title="Ship the release", priority="high", done=False, due_date=today),
            Task(
                title="Write the changelog",
                priority="medium",
                done=True,
                due_date=today - datetime.timedelta(days=2),
            ),
            Task(
                title="Review open PRs",
                priority="medium",
                done=False,
                due_date=today + datetime.timedelta(days=1),
            ),
            Task(title="Update dependencies", priority="low", done=True, due_date=None),
            Task(
                title="Fix flaky test",
                priority="high",
                done=False,
                due_date=today + datetime.timedelta(days=3),
            ),
        ]
    )


class DemoConfig(AppConfig):
    name = "demo"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self) -> None:
        post_migrate.connect(_seed_tasks, sender=self)
