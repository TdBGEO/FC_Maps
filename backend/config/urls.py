from django.contrib import admin
from django.urls import path, include

from .views import (
    EredivisieMapView,
    LandingView,
    WorldCupMapView,
    health_check,
)

urlpatterns = [
    path("", LandingView.as_view(), name="landing"),
    path("worldcup/", WorldCupMapView.as_view(), name="map-worldcup"),
    path("eredivisie/", EredivisieMapView.as_view(), name="map-eredivisie"),
    path("admin/", admin.site.urls),
    path("api/health/", health_check),
    path("api/", include("players.urls")),
    path("api/", include("squad.urls")),
]
