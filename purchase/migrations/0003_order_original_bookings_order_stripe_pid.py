# Generated by Django 4.0.6 on 2022-09-20 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("purchase", "0002_rename_town_or_city_order_city"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="original_bookings",
            field=models.TextField(default=""),
        ),
        migrations.AddField(
            model_name="order",
            name="stripe_pid",
            field=models.CharField(default="", max_length=254),
        ),
    ]