# Generated by Django 4.0.6 on 2022-09-13 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Meeja",
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
                ("my_image", models.ImageField(blank=True, upload_to="ot4u")),
            ],
        ),
    ]
