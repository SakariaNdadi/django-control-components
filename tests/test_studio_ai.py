from __future__ import annotations

import pytest
from django.core.exceptions import ValidationError

from django_control_components.studio.ai import draft_spec


class Provider:
    def __init__(self, result):
        self.result = result
        self.seen_palette = None

    def draft(self, *, prompt, palette):
        self.seen_palette = palette
        return self.result


def test_ai_draft_receives_palette_and_returns_json_copy():
    source = {"fields": [{"type": "TextInput", "name": "title"}]}
    provider = Provider(source)

    draft = draft_spec(provider, "Build an article form")
    source["fields"][0]["name"] = "changed"

    assert draft["fields"][0]["name"] == "title"
    assert any(item["name"] == "TextInput" for item in provider.seen_palette["fields"])


@pytest.mark.parametrize("result", [[], "text", {"callback": lambda: None}])
def test_ai_draft_rejects_non_json_output(result):
    with pytest.raises(ValidationError):
        draft_spec(Provider(result), "Build a form")


def test_ai_draft_rejects_empty_prompt():
    with pytest.raises(ValidationError, match="cannot be empty"):
        draft_spec(Provider({}), "  ")
