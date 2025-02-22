# Generated by Django 4.2.13 on 2024-07-08 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0005_alter_plan_subscription"),
    ]

    operations = [
        migrations.CreateModel(
            name="BuyPackage",
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
                ("email", models.CharField(max_length=100)),
                ("message", models.CharField(max_length=1000)),
            ],
            options={
                "verbose_name": "BuyPackage",
                "verbose_name_plural": "BuyPackages",
            },
        ),
    ]
