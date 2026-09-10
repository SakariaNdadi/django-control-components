from django.urls import include, path

from tests.e2e.views import nav_page

urlpatterns = [
    path("dcc/", include("django_control_components.urls")),
    path("studio/", include("django_control_components.studio.urls")),
    path("e2e/nav/", nav_page, name="e2e-nav"),
]
