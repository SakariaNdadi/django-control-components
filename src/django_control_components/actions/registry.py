"""Action addressing.

Security-critical. The client only ever sends an *owner key* and an *action
name*, both opaque strings registered at import / mount / render time. It never
sends an import path, a model label, or a callable. An unknown key is a 404.

An owner (a table) is rebuilt **per request** from a registered factory, so the
queryset an action is allowed to touch is always derived from the current
request. A tampered pk cannot reach a row this user was never shown, and one
tenant's render cannot leave a stale scope behind for another tenant's POST.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    from collections.abc import Callable

    from django.db.models import QuerySet
    from django.http import HttpRequest

    from .action import Action

    OwnerFactory = Callable[[HttpRequest], "ActionOwner"]


class ActionOwner(Protocol):
    @property
    def key(self) -> str: ...

    def get_action_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        """The rows this owner exposes for *this* request - the action scope."""

    def get_actions(self) -> dict[str, Action]: ...


class _Registry:
    def __init__(self) -> None:
        self._factories: dict[str, OwnerFactory] = {}

    def register(self, key: str, factory: OwnerFactory) -> None:
        """Register a per-request owner factory. ``factory(request)`` returns an
        owner scoped to that request. Registering the same key again replaces
        the factory - the caller is expected to pass an equivalent one."""
        self._factories[key] = factory

    def resolve(
        self, owner_key: str, action_name: str, request: HttpRequest
    ) -> tuple[ActionOwner, Action] | None:
        factory = self._factories.get(owner_key)
        if factory is None:
            return None
        owner = factory(request)
        action = owner.get_actions().get(action_name)
        if action is None:
            return None
        return owner, action

    def clear(self) -> None:
        self._factories.clear()


registry = _Registry()
