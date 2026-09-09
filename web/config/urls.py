from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from demo.panels import docs_panel

urlpatterns = [
    path("dcc/", include("django_control_components.urls")),
    docs_panel.mount(),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]

