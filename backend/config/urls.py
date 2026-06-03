from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.views.generic import TemplateView


def health_check(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="home"),
    path("admin/", admin.site.urls),
    path("api/health/", health_check),
    path("api/", include("players.urls")),
    path("api/", include("squad.urls")),
]