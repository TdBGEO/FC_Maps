from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import SquadView
from .serializers import SquadGeoSerializer


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
