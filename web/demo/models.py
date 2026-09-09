from django.db import models


class Task(models.Model):
    """The one model backing the "Full example" catalog page - just enough
    fields to show a Resource wiring a Table, a Schema and an Infolist
    together end to end."""

    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    title = models.CharField(max_length=200)
    done = models.BooleanField(default=False)
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    due_date = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title
