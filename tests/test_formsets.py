from __future__ import annotations

from django import forms

from django_control_components.schemas import FormSet, RelationManager, Schema, TextInput, Toggle
from tests.testapp.models import Article, Author, Comment


class NoteForm(forms.Form):
    title = forms.CharField()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["author_name", "body", "approved"]


def test_formset_renders_management_form_and_prefixed_fields():
    schema = Schema.make().form(NoteForm).strict().schema([TextInput.make("title")])
    component = FormSet.make(schema).rows(2).deletable().ordered()
    formset = component.build(prefix="notes")

    html = str(component.render(formset))

    assert 'name="notes-TOTAL_FORMS"' in html
    assert 'name="notes-0-title"' in html
    assert 'name="notes-1-title"' in html
    assert 'name="notes-0-DELETE"' in html
    assert 'name="notes-0-ORDER"' in html


def test_formset_uses_django_validation():
    schema = Schema.make().form(NoteForm).strict().schema([TextInput.make("title")])
    component = FormSet.make(schema).rows(1).minimum(1)
    formset = component.build(
        {"form-TOTAL_FORMS": "1", "form-INITIAL_FORMS": "0", "form-0-title": ""}
    )

    assert not formset.is_valid()
    assert "Please submit at least 1 form" in str(component.render(formset))


def test_relation_manager_builds_valid_inline_formset(db):
    author = Author.objects.create(name="Ada")
    article = Article.objects.create(title="T", slug="t", author=author)
    schema = (
        Schema.make()
        .form(CommentForm)
        .strict()
        .schema([TextInput.make("author_name"), TextInput.make("body"), Toggle.make("approved")])
    )
    manager = RelationManager.make(Article, Comment, schema).rows(1).deletable()
    formset = manager.build(
        article,
        {
            "comments-TOTAL_FORMS": "1",
            "comments-INITIAL_FORMS": "0",
            "comments-MIN_NUM_FORMS": "0",
            "comments-MAX_NUM_FORMS": "1000",
            "comments-0-author_name": "Grace",
            "comments-0-body": "Looks good",
            "comments-0-approved": "on",
        },
    )

    assert formset.is_valid(), formset.errors
    saved = formset.save()
    assert saved[0].article == article
    assert article.comments.get().author_name == "Grace"
