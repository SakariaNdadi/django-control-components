"""View mixin for table pages."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.http import HttpResponse

from .. import htmx

if TYPE_CHECKING:
    from .table import Table


class TableMixin:
    """Render a :class:`Table` and answer htmx partial-swap requests.

    Set ``table`` or override ``get_table()``. On an ``HX-Request`` carrying the
    table's marker the mixin returns only the content fragment; otherwise the
    full page renders and the table appears via ``{{ table_html }}``.

    Place this mixin *before* any auth mixin so ``dispatch`` still runs the auth
    check first (the partial is served from ``get``, after ``dispatch``).
    """

    table: Table | None = None
    table_context_name = "table_html"

    def get_table(self) -> Table:
        if self.table is None:
            raise ValueError(f"{type(self).__name__} needs a `table` or `get_table()`")
        return self.table

    def _prepared_table(self) -> Table:
        """``get_table()`` plus a per-request owner factory, so the action
        endpoint re-scopes against the requesting user rather than trusting the
        table instance that rendered last. The factory rebuilds this view for
        the action request and calls ``get_table()`` again - so a ``get_table``
        that reads only ``self.request`` is safe; one that also depends on URL
        kwargs should register its own factory."""
        table = self.get_table()
        if table._owner_factory is None:
            view_cls = type(self)

            def factory(request: Any) -> Table:
                view = view_cls()
                view.setup(request)  # type: ignore[attr-defined]
                return view.get_table()

            table.set_owner_factory(factory)
        return table

    def get(self, request: Any, *args: Any, **kwargs: Any) -> HttpResponse:
        table = self._prepared_table()
        if htmx.is_htmx(request) and request.GET.get("_dcc_table") == table.table_id:
            return HttpResponse(table.render_content(request))
        return super().get(request, *args, **kwargs)  # type: ignore[misc]

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)  # type: ignore[misc]
        context[self.table_context_name] = self._prepared_table().render(self.request)  # type: ignore[attr-defined]
        return context
