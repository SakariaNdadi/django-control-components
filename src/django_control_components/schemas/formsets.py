"""Django-native formset and inline relation rendering."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

from django.forms import BaseFormSet, ModelForm, formset_factory, inlineformset_factory
from django.forms.models import BaseInlineFormSet
from django.template.loader import render_to_string
from django.utils.safestring import SafeString

if TYPE_CHECKING:
    from django.db.models import Model
    from django.http import HttpRequest

    from .schema import Schema


class _FormCollection:
    def __init__(self, schema: Schema) -> None:
        self.schema = schema
        self.extra = 1
        self.can_delete = False
        self.can_order = False
        self.min_num = 0
        self.max_num = 1000

    def rows(self, value: int) -> Self:
        if value < 0:
            raise ValueError("FormSet.rows() must be zero or greater")
        self.extra = value
        return self

    def deletable(self, value: bool = True) -> Self:
        self.can_delete = value
        return self

    def ordered(self, value: bool = True) -> Self:
        self.can_order = value
        return self

    def minimum(self, value: int) -> Self:
        if value < 0:
            raise ValueError("FormSet.minimum() must be zero or greater")
        self.min_num = value
        return self

    def maximum(self, value: int) -> Self:
        if value < 1:
            raise ValueError("FormSet.maximum() must be greater than zero")
        self.max_num = value
        return self

    def render(
        self, formset: BaseFormSet[Any], *, request: HttpRequest | None = None
    ) -> SafeString:
        rows = []
        for form in formset.forms:
            instance = getattr(form, "instance", None)
            rows.append(
                {
                    "schema_html": self.schema.render(
                        request=request,
                        form=form,
                        record=instance,
                        operation="edit" if getattr(instance, "pk", None) else "create",
                    ),
                    "delete_field": form["DELETE"] if self.can_delete else None,
                    "order_field": form["ORDER"] if self.can_order else None,
                }
            )
        return SafeString(
            render_to_string(
                "django_control_components/formsets/formset.html",
                {
                    "management_form": formset.management_form,
                    "non_form_errors": formset.non_form_errors(),
                    "rows": rows,
                },
                request=request,
            )
        )


class FormSet(_FormCollection):
    """Build and render repeated instances of one schema using Django forms."""

    @classmethod
    def make(cls, schema: Schema) -> Self:
        return cls(schema)

    def get_formset_class(self) -> type[BaseFormSet[Any]]:
        return formset_factory(
            self.schema.get_form_class(),
            extra=self.extra,
            can_delete=self.can_delete,
            can_order=self.can_order,
            min_num=self.min_num,
            max_num=self.max_num,
            validate_min=True,
            validate_max=True,
        )

    def build(self, data: Any = None, files: Any = None, **kwargs: Any) -> BaseFormSet[Any]:
        return self.get_formset_class()(data=data, files=files, **kwargs)


class RelationManager(_FormCollection):
    """Manage a parent/child relation through Django's inline formsets."""

    def __init__(
        self,
        parent_model: type[Model],
        related_model: type[Model],
        schema: Schema,
        *,
        fk_name: str | None = None,
    ) -> None:
        super().__init__(schema)
        self.parent_model = parent_model
        self.related_model = related_model
        self.fk_name = fk_name

    @classmethod
    def make(
        cls,
        parent_model: type[Model],
        related_model: type[Model],
        schema: Schema,
        *,
        fk_name: str | None = None,
    ) -> Self:
        return cls(parent_model, related_model, schema, fk_name=fk_name)

    def get_formset_class(self) -> type[BaseInlineFormSet[Any, Any]]:
        form_class = self.schema.get_form_class()
        if not issubclass(form_class, ModelForm):
            raise ValueError("RelationManager schema must use a Django ModelForm")
        return inlineformset_factory(
            self.parent_model,
            self.related_model,
            form=form_class,
            fk_name=self.fk_name,
            extra=self.extra,
            can_delete=self.can_delete,
            min_num=self.min_num,
            max_num=self.max_num,
            validate_min=True,
            validate_max=True,
        )

    def build(
        self, instance: Model, data: Any = None, files: Any = None, **kwargs: Any
    ) -> BaseInlineFormSet[Any, Any]:
        return self.get_formset_class()(data=data, files=files, instance=instance, **kwargs)
