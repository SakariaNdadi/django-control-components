# Website

The package's live site and documentation demo. A `docs` panel (mounted at the
site root) with one hand-written page per builder plus a live component catalog —
every primitive rendered next to its source, backed by a real `Task` model.

```bash
# from the repo root
uv sync
uv run --project web python web/manage.py migrate   # builds an ephemeral SQLite db and seeds demo rows
uv run --project web python web/manage.py runserver
```

Open <http://127.0.0.1:8000/>. No login is required. The database
(`web/db.sqlite3`) is throwaway — gitignored and rebuilt by `migrate`, which
fills an empty db with demo `Task` rows via a `post_migrate` hook in
`demo/apps.py`.

## What to try

| Route | What it shows |
|---|---|
| `/` | Catalog home — links every component page, grouped by family |
| `/installation/`, `/quickstart/` | Prose intro pages |
| `/table/`, `/schema/`, `/select/`, `/modal/`, `/chart-widget/`, … | One page per primitive: live render beside its source. Full list in the sidebar. |
| `/task/` | A live `Resource` — list · create · edit · view · delete against the `Task` table, with a filter, search, sort, and a declared infolist |
| `/full-example/` | The `TaskResource` walkthrough — Table + Schema + Infolist wired end to end |
| `/wizards/` | An interactive session-backed 3-step htmx wizard with per-step Django validation and a review infolist |
| `/panels-and-resources/` | How `Panel` / `Resource` / `Widget` compose |

## Reseeding

Delete `web/db.sqlite3` and rerun `migrate` — the `post_migrate` hook refills it.

## Large-dataset mode

Lower `DCC["TABLE_CLIENT_SIDE_MAX_ROWS"]` in `web/config/settings.py` to push a
table into server mode: the first page renders, then a sentinel row appends the
next batch as you scroll. Watch the query log — there is no `SELECT COUNT(*)`.
