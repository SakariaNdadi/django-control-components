from __future__ import annotations

from typing import Any

from django.http import Http404, HttpRequest, HttpResponse
from django.views import View

from .. import htmx
from ..core.component import UNSET
from .registry import registry


class ActionView(View):
    """Single endpoint for every registered action.

    GET  -> render the confirmation / schema modal.
    POST -> authorize (again), re-scope targets to the owner's queryset, execute.
    """

    def _resolve(
        self, request: HttpRequest, owner_key: str, action_name: str
    ) -> tuple[Any, Any]:
        found = registry.resolve(owner_key, action_name, request)
        if found is None:
            raise Http404("Unknown action")
        return found

    @staticmethod
    def _baseline_denied(request: HttpRequest, action: Any) -> bool:
        """This endpoint is mounted outside any panel, so it has no guard of its
        own. An action with no ``.authorize()`` rule is implicitly allowed
        (``ACTIONS_DEFAULT_DENY`` defaults to ``False``), which would make it
        runnable by an anonymous POST. Refuse that here - an action that really
        is public says so with an explicit ``.authorize(...)`` rule, which
        ``is_authorized`` then evaluates as usual."""
        if action._config.get("authorize", UNSET) is not UNSET:
            return False
        user = getattr(request, "user", None)
        return user is None or not user.is_authenticated

    def _targets(self, request: HttpRequest, owner: Any, action: Any) -> Any:
        scope = owner.get_action_queryset(request)
        if action.is_bulk:
            select_all = (
                request.POST.get("select_all") == "1" or request.GET.get("select_all") == "1"
            )
            if select_all:
                # "every row matching the current filter" - the owner already
                # scoped `scope` to those filters. Hand back the queryset itself
                # (unmaterialised) so a callback can `.update()` it in one query.
                return scope
            ids = request.POST.getlist("records") or request.GET.getlist("records")
            if not ids:
                return []
            # re-scope: intersect requested ids with what the owner exposes
            return list(scope.filter(pk__in=ids))
        raw = request.POST.get("record") or request.GET.get("record")
        if raw is None:
            return []
        obj = scope.filter(pk=raw).first()
        if obj is None:
            # a pk was named but it is not in this request's scope - stale page
            # or a tampered id. Do not fall through to running the action.
            raise Http404("Record not in scope")
        return [obj]

    def get(self, request: HttpRequest, owner_key: str, action_name: str) -> HttpResponse:
        owner, action = self._resolve(request, owner_key, action_name)
        records = self._targets(request, owner, action)
        if self._baseline_denied(request, action) or not action.is_authorized(
            request, records[0] if records else None
        ):
            return HttpResponse(status=403)

        form_html: Any = ""
        schema = action._config.get("schema")
        if schema is not None:
            instance = records[0] if records and not action.is_bulk else None
            form_html = schema.render(
                request=request, form=schema.build_standalone_form(instance=instance)
            )
        else:
            content = action._config.get("modal_content")
            if callable(content):
                from ..core.context import RenderContext
                from ..core.evaluate import evaluate

                form_html = evaluate(
                    content,
                    RenderContext(request=request, record=records[0] if records else None),
                )
        return HttpResponse(
            action.render_modal(request=request, records=records, form_html=form_html)
        )

    def post(self, request: HttpRequest, owner_key: str, action_name: str) -> HttpResponse:
        owner, action = self._resolve(request, owner_key, action_name)
        records = self._targets(request, owner, action)
        if self._baseline_denied(request, action) or not action.is_authorized(
            request, records[0] if records else None
        ):
            return HttpResponse(status=403)

        data: dict[str, Any] = {}
        schema = action._config.get("schema")
        if schema is not None:
            instance = records[0] if records and not action.is_bulk else None
            form = schema.build_standalone_form(
                data=request.POST, files=request.FILES, instance=instance
            )
            if not form.is_valid():
                return HttpResponse(
                    action.render_modal(
                        request=request,
                        records=records,
                        form_html=schema.render(request=request, form=form),
                    )
                )
            data = form.cleaned_data

        action.run(request, records, data)

        # A modal action must clear its mount so the dialog closes; htmx will not
        # swap on 204, so hand back an empty 200 for those. Inline actions keep
        # 204 (their row must not be blanked) and rely on dcc:refresh to repaint.
        resp = HttpResponse("") if action.needs_modal else HttpResponse(status=204)
        return htmx.response.trigger(
            resp,
            {"dcc:toast": action.success_message(), "dcc:refresh": True},
        )
