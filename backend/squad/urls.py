from rest_framework.routers import DefaultRouter
from .views import SquadViewSet

router = DefaultRouter()
router.register(r"squad", SquadViewSet, basename="squad")

urlpatterns = router.urls
