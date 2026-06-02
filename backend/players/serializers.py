from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Player


class PlayerGeoSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = Player
        geo_field = "geom"
        fields = [
            "ogc_fid",
            "naam",
            "geom",
            "club",
            "nationality_text",
            "match_addr",
            "nationality_iso3",
            "birthplace_iso3",
        ]