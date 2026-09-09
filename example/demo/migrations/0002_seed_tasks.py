import datetime

from django.db import migrations


def seed(apps, schema_editor):
    Task = apps.get_model("demo", "Task")
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


def unseed(apps, schema_editor):
    Task = apps.get_model("demo", "Task")
    Task.objects.filter(
        title__in=[
            "Ship the release",
            "Write the changelog",
            "Review open PRs",
            "Update dependencies",
            "Fix flaky test",
        ]
    ).delete()


class Migration(migrations.Migration):
    dependencies = [("demo", "0001_initial")]
    operations = [migrations.RunPython(seed, unseed)]
