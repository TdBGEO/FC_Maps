from django.contrib.gis import admin
from .models import Player


@admin.register(Player)
class PlayerAdmin(admin.GISModelAdmin):
    list_display = ["naam", "club", "nationality_text", "match_addr"]
    list_filter = ["nationality_text", "club"]
    search_fields = ["naam", "club", "match_addr"]
    readonly_fields = ["ogc_fid"]