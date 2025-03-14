# Generated by Django 5.1.7 on 2025-03-10 19:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("modules", "0003_alter_rating_user_delete_user"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
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
                ("username", models.CharField(default="", max_length=30)),
                ("email", models.CharField(default="", max_length=30)),
                ("password", models.CharField(default="", max_length=30)),
                ("logged_in", models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name="rating",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="modules.user"
            ),
        ),
    ]
