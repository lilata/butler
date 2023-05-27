# Generated by Django 4.2.1 on 2023-05-27 21:34

from django.db import migrations, models

import core.models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_comment"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProtectedFile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.TextField()),
                (
                    "file",
                    models.FileField(upload_to=core.models.protected_file_upload_to),
                ),
            ],
        ),
    ]
