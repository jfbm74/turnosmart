# Generated by Django 5.1.5 on 2025-01-27 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("configuracion", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="ticket",
            name="nombre",
            field=models.CharField(default="principal", max_length=255),
            preserve_default=False,
        ),
    ]
