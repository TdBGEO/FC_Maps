from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import SquadView


class SquadGeoSerializer(GeoFeatureModelSerializer):

    class Meta:
        model     = SquadView
        geo_field = "geom"
        fields = [
            "player_code",
            "name",
            "date_of_birth",
            "birth_country_iso3",
            "birth_country",
            "birthplace_city",
            "match_addr",
            "geom",
            "position",
            "club",
            "club_competition",
            "national_team",
            "country_iso3",
            "competition",
            "competition_code",
            "is_active",
        ]