# Website

The package's live site and documentation demo. A complete app that exercises
every builder — schema forms, an auto client/server data table, row & bulk
actions, a htmx wizard, panels with widgets and a custom page, and a **no-code**
resource defined entirely from stored JSON.

```bash
# from the repo root
uv sync
uv run --project web python web/manage.py migrate   # builds an ephemeral SQLite db and seeds demo rows
uv run --project web python web/manage.py runserver
```

Open <http://127.0.0.1:8000/>. The dashboard links every feature; no login is
required. The database (`web/db.sqlite3`) is throwaway — it is gitignored and
rebuilt by `migrate`, which fills an empty db with demo `Task` rows via a
`post_migrate` hook in `demo/apps.py`.

## What to try

| Page | What it shows |
|---|---|
| **Dashboard** `/` | Feature hub + KPI tiles |
| **Component gallery** `/components/` | Every primitive: buttons, badges, icons, modal, menu, all form controls |
| **Articles table** `/articles/` | Status / Featured filters, search, sort, pagination — all zero-request at 60 rows. Tick rows → bulk bar → **"Mark live"** confirm modal → toast + refresh; **"Select every matching row"** for bulk over the whole filter. Row actions: **Edit** (navigates), **Quick edit** (schema form in a modal), **Toggle ★** (inline). |
| **New / Edit article** `/articles/new/` | Sections, **searchable** selects, `published_at` appears only when Status = Live, Pillow-validated image upload. Submit with JavaScript disabled — still validates. |
| **Publish wizard** `/wizard/` | Steps advance over **htmx** (no full-page reload); per-step Django validation; `Back` and no-JS still work. |
| **Panel** `/panel/` | Dashboard with **stat / chart / table widgets**; a custom **Reports** page (`Panel.pages`); Article & Author resources with list · create · edit · view · **delete** and a declared **infolist** on the view page. |
| **Comments (no-code)** `/panel/d/comments/` | A full resource — table, form, infolist — defined by one stored `DashboardSpec` JSON row. No Python subclass. |
| **Django admin** `/admin/` | Same credentials; runs alongside the panel, untouched |

## Reseeding

Delete `web/db.sqlite3` and rerun `migrate` — the `post_migrate` hook refills it.

## Large-dataset mode

Lower `DCC["TABLE_CLIENT_SIDE_MAX_ROWS"]` in `web/config/settings.py` to push a
table into server mode: the first page renders, then a sentinel row appends the
next batch as you scroll. Watch the query log — there is no `SELECT COUNT(*)`.
