"""URL map for the e2e settings: our hand-built interactive pages, the studio
builder mount, then the demo panel (catch-all at ``""``) last.
"""

from __future__ import annotations

from demo.panels import docs_panel
from django.contrib import admin
from django.urls import include, path

from tests.e2e import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("dcc/", include("django_control_components.urls")),
    path("studio/", include("django_control_components.studio.urls")),
    path("e2e/nav/", views.nav_page, name="e2e-nav"),
    path("e2e/shell/", views.shell_page, name="e2e-shell"),
    path("e2e/toasts/", views.toasts_page, name="e2e-toasts"),
    path("e2e/modal/", views.modal_page, name="e2e-modal"),
    path("e2e/menu/", views.menu_page, name="e2e-menu"),
    path("e2e/tabs/", views.tabs_page, name="e2e-tabs"),
    path("e2e/form/", views.form_page, name="e2e-form"),
    path("e2e/cotton/", views.cotton_tags_page, name="e2e-cotton"),
    path("e2e/table/", views.table_page, name="e2e-table"),
    path("e2e/blocks/", views.blocks_page, name="e2e-blocks"),
    path("e2e/search-api/", views.search_api, name="e2e-search-api"),
    path("e2e/bell-api/", views.bell_api, name="e2e-bell-api"),
    docs_panel.mount(),
]
