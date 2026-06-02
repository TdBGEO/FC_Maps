"""
API views for the players app.

"""

from rest_framework import viewsets, filters
from .models import Player
from .serializers import PlayerGeoSerializer


class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list:   GET /api/players/           — returns all players as GeoJSON FeatureCollection
    detail: GET /api/players/{id}/      — returns a single player as GeoJSON Feature
    """

    queryset = Player.objects.all()
    serializer_class = PlayerGeoSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["naam", "club", "nationality_text", "match_addr"]
    ordering_fields = ["naam", "club", "nationality_text"]
