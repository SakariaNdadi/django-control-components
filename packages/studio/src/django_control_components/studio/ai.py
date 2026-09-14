"""Provider-neutral, non-executing AI draft seam for Studio specifications."""

from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING, Any, Protocol

from django.core.exceptions import ValidationError

from .deserialize import _check_jsonable, _check_size_and_depth
from .palette import palette

if TYPE_CHECKING:
    from django.http import HttpRequest


class SpecDraftProvider(Protocol):
    """A provider that returns data only; it never receives executable objects."""

    def draft(self, *, prompt: str, palette: dict[str, list[dict[str, Any]]]) -> Any: ...


def draft_spec(
    provider: SpecDraftProvider,
    prompt: str,
    *,
    request: HttpRequest | None = None,
) -> dict[str, Any]:
    """Return a bounded JSON draft for later Studio validation and preview."""
    if not prompt.strip():
        raise ValidationError("AI specification prompt cannot be empty")
    result = provider.draft(prompt=prompt, palette=deepcopy(palette(request)))
    if not isinstance(result, dict):
        raise ValidationError("AI specification provider must return a JSON object")
    _check_size_and_depth(result)
    _check_jsonable(result, "AI specification draft")
    return deepcopy(result)


__all__ = ["SpecDraftProvider", "draft_spec"]
