# Generated by Django 4.1.6 on 2023-02-07 00:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pets", "0002_pet_group"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pet",
            name="sex",
            field=models.CharField(
                choices=[
                    ("Male", "Male"),
                    ("Female", "Female"),
                    ("Not Informed", "Default"),
                ],
                default="Not Informed",
                max_length=20,
            ),
        ),
    ]
