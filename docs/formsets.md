# Formsets and relation managers

These builders decorate Django formsets; Django owns binding, management-form
validation, deletion, ordering, and saving.

```python
notes = FormSet.make(note_schema).rows(2).minimum(1).deletable()
formset = notes.build(request.POST or None, prefix="notes")
html = notes.render(formset, request=request)
```

For a reverse foreign-key relation, use a `ModelForm` schema:

```python
comments = RelationManager.make(Article, Comment, comment_schema).rows(1).deletable()
formset = comments.build(article, request.POST or None)
if formset.is_valid():
    formset.save()
```

The first slice is server-rendered. Dynamic HTMX row insertion, nested
relations, permission-aware resource integration, and Studio serialization are
planned on top of this contract.
