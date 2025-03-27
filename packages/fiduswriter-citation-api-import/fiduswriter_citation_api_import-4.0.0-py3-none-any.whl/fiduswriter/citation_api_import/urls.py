from django.urls import re_path

from . import views

urlpatterns = [
    re_path(
        "^proxy/(?P<url>.*)$", views.proxy, name="citation_api_import_proxy"
    ),
]
