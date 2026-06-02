from django.contrib.gis.db import models


class SquadView(models.Model):
    """
    Read-only model mapping to data.squad_view.
    Django never creates or alters this — it's a PostgreSQL view.
    """
    player_code      = models.TextField(primary_key=True)
    name             = models.TextField()
    date_of_birth    = models.DateField(null=True, blank=True)
    birth_country_iso3 = models.CharField(max_length=3, null=True, blank=True)
    birth_country    = models.TextField(null=True, blank=True)
    birthplace_city  = models.TextField(null=True, blank=True)
    match_addr       = models.TextField(null=True, blank=True)
    geom             = models.PointField(srid=4326, null=True, blank=True)
    position         = models.TextField(null=True, blank=True)
    season_id        = models.IntegerField(null=True, blank=True)
    club             = models.TextField(null=True, blank=True)
    club_competition = models.TextField(null=True, blank=True)
    national_team    = models.TextField(null=True, blank=True)
    country_iso3     = models.CharField(max_length=3, null=True, blank=True)
    competition      = models.TextField(null=True, blank=True)
    competition_code = models.TextField(null=True, blank=True)
    is_active        = models.BooleanField(null=True, blank=True)

    class Meta:
        db_table = '"data"."squad_view"'
        managed  = False
        ordering = ["name"]
        verbose_name        = "Squad Player"
        verbose_name_plural = "Squad Players"

    def __str__(self):
        return self.name