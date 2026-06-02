from django.contrib.gis.db import models


class Player(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    geom = models.PointField(srid=4326, null=True, blank=True)
    objectid = models.IntegerField(null=True, blank=True)
    naam = models.CharField(max_length=255, blank=True, default="")
    club = models.CharField(max_length=255, blank=True, default="")
    nationality_text = models.CharField(max_length=255, blank=True, default="")
    match_addr = models.CharField(max_length=255, blank=True, default="")
    nationality_iso3 = models.CharField(max_length=10, blank=True, default="")
    birthplace_iso3 = models.CharField(max_length=10, blank=True, default="")

    class Meta:
        db_table = '"ref"."place"'
        managed = False
        ordering = ["naam"]
        verbose_name = "Player"
        verbose_name_plural = "Players"

    def __str__(self) -> str:
        return self.naam