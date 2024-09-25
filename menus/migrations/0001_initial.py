# Generated by Django 5.0.6 on 2024-09-24 19:22

import menus.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "category_id",
                    models.SmallAutoField(primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=20, unique=True)),
            ],
            options={
                "db_table": "category",
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "product_id",
                    models.SmallAutoField(primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=40, unique=True)),
                ("price", models.PositiveIntegerField()),
                ("stock", models.PositiveSmallIntegerField()),
                ("is_active", models.BooleanField(default=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=models.SET(menus.models.get_sentinel_category),
                        related_name="products",
                        to="menus.category",
                    ),
                ),
            ],
            options={
                "db_table": "product",
            },
        ),
    ]