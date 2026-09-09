"""Turn a validated :class:`TableState` into a queryset.

Security-critical: no querystring value is ever passed to ``order_by`` or
``filter`` as a key. A requested sort must name a column that declared itself
sortable; the ORM path then comes from that column. Search builds a ``Q`` over
the columns that declared themselves searchable, nothing else.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.core.exceptions import FieldDoesNotExist
from django.db.models import Q, QuerySet

if TYPE_CHECKING:
    from .columns import Column
    from .filters import Filter
    from .state import TableState


def related_hints(model: type[Any], columns: list[Column]) -> tuple[list[str], list[str]]:
    """``(select_related, prefetch_related)`` paths derived from the columns'
    dotted names, so a table with FK columns does not N+1 per row.

    Each dotted column contributes the relation path up to (not including) its
    final attribute. A segment that is a forward single-valued relation goes to
    ``select_related``; a many-valued one switches the whole path to
    ``prefetch_related``; a segment that is not an ORM field at all (a
    ``.state(fn)`` column whose ``name`` is not a real path) is ignored.
    """
    select: list[str] = []
    prefetch: list[str] = []
    for column in columns:
        if "." not in column.name:
            continue
        *relation_parts, _leaf = column.name.split(".")
        current = model
        orm_path: list[str] = []
        many = False
        ok = True
        for part in relation_parts:
            try:
                field = current._meta.get_field(part)
            except FieldDoesNotExist:
                ok = False
                break
            if not field.is_relation:
                ok = False
                break
            orm_path.append(part)
            if field.many_to_many or field.one_to_many:
                many = True
            related = getattr(field, "related_model", None)
            if related is None:
                ok = False
                break
            current = related
        if not ok or not orm_path:
            continue
        path = "__".join(orm_path)
        (prefetch if many else select).append(path)
    return sorted(set(select)), sorted(set(prefetch))


def apply_sort(queryset: QuerySet[Any], state: TableState, columns: list[Column]) -> QuerySet[Any]:
    if not state.sort:
        return queryset
    sortable = {c.name: c for c in columns if c.is_sortable}
    column = sortable.get(state.sort)
    if column is None:
        return queryset
    field = column.sort_field()
    return queryset.order_by(f"-{field}" if state.descending else field)


def apply_search(
    queryset: QuerySet[Any], state: TableState, columns: list[Column]
) -> QuerySet[Any]:
    if not state.search:
        return queryset
    predicate = Q()
    for column in columns:
        if not column.is_searchable:
            continue
        for path in column.search_fields():
            predicate |= Q(**{f"{path}__icontains": state.search})
    if not predicate:
        return queryset
    return queryset.filter(predicate)


def apply_filters(
    queryset: QuerySet[Any], state: TableState, filters: list[Filter]
) -> QuerySet[Any]:
    by_name = {f.name: f for f in filters}
    for name, raw in state.filters.items():
        f = by_name.get(name)
        if f is not None:
            queryset = f.apply(queryset, raw)
    return queryset


def apply_all(
    queryset: QuerySet[Any],
    state: TableState,
    columns: list[Column],
    filters: list[Filter],
    *,
    with_related: bool = True,
) -> QuerySet[Any]:
    queryset = apply_filters(queryset, state, filters)
    queryset = apply_search(queryset, state, columns)
    queryset = apply_sort(queryset, state, columns)
    if with_related:
        select, prefetch = related_hints(queryset.model, columns)
        if select:
            queryset = queryset.select_related(*select)
        if prefetch:
            queryset = queryset.prefetch_related(*prefetch)
    return queryset
