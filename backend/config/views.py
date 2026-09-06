"""
Page views for FC Maps.

The API lives in the `squad` app; this module only serves the HTML pages: the
landing page and the two map pages. Both maps render the same template
(`base_map.html`) and differ purely in the context assembled here, so a styling
or behaviour fix lands on both at once.
"""

from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import JsonResponse
from django.urls import reverse
from django.views.generic import TemplateView

SITE_URL = "https://fcmaps.nl"

CLUB_BADGE_DIR = "clubs"


def health_check(request):
    return JsonResponse({"status": "ok"})


def club_badges():
    """
    Map every club badge slug to its served URL, e.g.
    {"ajax-amsterdam": "/static/clubs/ajax-amsterdam.a1b2c3d4.png"}

    The URLs must be resolved here rather than built in JavaScript:
    STATICFILES_STORAGE is CompressedManifestStaticFilesStorage, which renames
    files with a content hash at collectstatic time, so a hand-built
    "/static/clubs/ajax-amsterdam.png" would 404 in production.

    We read the source directory rather than the manifest so a badge dropped
    into backend/static/clubs/ is picked up with no code change.
    """
    badge_dir = settings.BASE_DIR / "static" / CLUB_BADGE_DIR
    if not badge_dir.is_dir():
        return {}

    badges = {}
    for path in sorted(badge_dir.glob("*.png")):
        badges[path.stem] = staticfiles_storage.url(f"{CLUB_BADGE_DIR}/{path.name}")
    return badges


class LandingView(TemplateView):
    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            page_title="FC Maps: The football atlas of the world",
            page_url=f"{SITE_URL}/",
            meta_description=(
                "FC Maps plots where professional footballers were born. "
                "Explore the FIFA World Cup 2026 squads and the Dutch Eredivisie 2026/27."
            ),
            **kwargs,
        )


class BaseMapView(TemplateView):
    """
    Shared plumbing for a map page.

    Subclasses set the class attributes below; `map_config` is the subset that
    is handed to the browser as JSON (see base_map.html).
    """

    competition_code = ""
    season_label = ""
    marker_mode = "national_flag"  # or "club_badge"
    stats_group_field = "club_competition"
    club_cascade = True
    show_country_filter = True
    entity_panel_label = "COUNTRY"
    stats_group_label = "Top club leagues"
    default_view = (20, 0, 2)  # lat, lng, zoom — used when there is nothing to fit
    # Club maps add a "top cities of birth" list; on the WC map birthplaces are
    # spread worldwide and the country list already tells that story.
    show_city_stats = False
    # Rendered as "{empty_title} {empty_title_accent}", the accent in orange.
    # Kept as two plain strings so the template needs no |safe.
    empty_title = ""
    empty_title_accent = ""
    empty_message = ""

    def map_config(self):
        return {
            "competition_code": self.competition_code,
            "marker_mode": self.marker_mode,
            "stats_group_field": self.stats_group_field,
            "club_cascade": self.club_cascade,
            "season_label": self.season_label,
            "default_view": list(self.default_view),
            "club_badges": club_badges() if self.marker_mode == "club_badge" else {},
            "show_city_stats": self.show_city_stats,
            "carto_key": settings.CARTO_BASEMAP_KEY,
        }

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            map_config=self.map_config(),
            season_label=self.season_label,
            club_cascade=self.club_cascade,
            show_country_filter=self.show_country_filter,
            entity_panel_label=self.entity_panel_label,
            stats_group_label=self.stats_group_label,
            empty_title=self.empty_title,
            empty_title_accent=self.empty_title_accent,
            empty_message=self.empty_message,
            **kwargs,
        )


class WorldCupMapView(BaseMapView):
    template_name = "worldcup.html"

    competition_code = "WC2026"
    season_label = "WC 2026"
    marker_mode = "national_flag"
    stats_group_field = "club_competition"
    club_cascade = True
    show_country_filter = True
    entity_panel_label = "COUNTRY"
    stats_group_label = "Top club leagues"
    default_view = (20, 0, 2)
    empty_title = "No players"
    empty_title_accent = "loaded"
    # On this map an empty result means something went wrong, not "not yet".
    empty_message = (
        "The squad data could not be loaded right now. Please try again in a moment."
    )

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            page_title="FC Maps — World Cup 2026",
            page_url=f"{SITE_URL}{reverse('map-worldcup')}",
            og_description=(
                "An interactive atlas of FIFA World Cup 2026 player birthplaces. "
                "Filter by country, club competition, position and more."
            ),
            twitter_description=(
                "An interactive atlas of FIFA World Cup 2026 player birthplaces."
            ),
            meta_description=(
                "Interactive map showing where every player in every qualified squad "
                "for FIFA World Cup 2026 was born. Filter by country, club, league, and more."
            ),
            **kwargs,
        )


class EredivisieMapView(BaseMapView):
    template_name = "eredivisie.html"

    competition_code = "ERE2627"
    season_label = "EREDIVISIE 2026/27"
    marker_mode = "club_badge"
    # Every row is the same league, so "top club leagues" would be a list of one.
    # Club counts are near-uniform (~26 a squad) and say nothing interesting, so
    # this map ranks nationalities instead.
    stats_group_field = "nationality"
    show_city_stats = True
    club_cascade = False
    # Club rosters carry no national team, so that filter has nothing to offer.
    show_country_filter = False
    entity_panel_label = "CLUB"
    stats_group_label = "Top nationalities"
    default_view = (52.15, 5.4, 7)  # the Netherlands
    empty_title = "Squads arrive"
    empty_title_accent = "soon"
    empty_message = (
        "Eredivisie 2026/27 rosters are added once the season is under way. "
        "The map will fill in as squads are confirmed."
    )

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            page_title="FC Maps — Eredivisie 2026/27",
            page_url=f"{SITE_URL}{reverse('map-eredivisie')}",
            og_description=(
                "An interactive atlas of Eredivisie 2026/27 player birthplaces. "
                "Filter by club, position and country of birth."
            ),
            twitter_description=(
                "An interactive atlas of Eredivisie 2026/27 player birthplaces."
            ),
            meta_description=(
                "Interactive map showing where every player in every Eredivisie 2026/27 "
                "club squad was born. Filter by club, position, and country of birth."
            ),
            empty_cta_url=reverse("map-worldcup"),
            empty_cta_label="View the World Cup map →",
            **kwargs,
        )
