"""
Initial migration for the Player model.
Requires PostGIS extension (created automatically by the postgis/postgis Docker image).
"""

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Player",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("birthplace", django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ("birth_city", models.CharField(blank=True, default="", max_length=255)),
                ("birth_country", models.CharField(blank=True, default="", max_length=255)),
                ("nationality", models.CharField(blank=True, default="", max_length=255)),
                ("club", models.CharField(blank=True, default="", max_length=255)),
                ("position", models.CharField(blank=True, default="", max_length=100)),
                ("date_of_birth", models.DateField(blank=True, null=True)),
            ],
            options={
                "verbose_name": "Player",
                "verbose_name_plural": "Players",
                "ordering": ["name"],
            },
        ),
    ]