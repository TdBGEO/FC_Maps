from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import SquadView
from .serializers import SquadGeoSerializer


# Cache list responses for 5 minutes — data only changes when we manually sync,
# so stale-ness up to 5 min is fine and saves a massive amount of DB load.
CACHE_SECONDS = 60 * 5


@method_decorator(cache_page(CACHE_SECONDS), name="list")
@method_decorator(vary_on_headers("Accept-Encoding"), name="list")
class SquadViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SquadGeoSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = [
        "competition_code",
        "country_iso3",
        "club_competition",
        "position",
        "is_active",
        "birth_country_iso3",
    ]
    search_fields = ["name", "club", "birthplace_city", "birth_country"]
    ordering_fields = ["name", "country_iso3", "club", "position"]

    def get_queryset(self):
        return SquadView.objects.all()