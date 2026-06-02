"""
URL routing for the players app.
Mounted under /api/ in config/urls.py, so full paths are:
  /api/players/       — list
  /api/players/{id}/  — detail
"""

from rest_framework.routers import DefaultRouter
from .views import PlayerViewSet

router = DefaultRouter()
router.register(r"players", PlayerViewSet, basename="player")

urlpatterns = router.urls