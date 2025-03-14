# Generated by Django 5.1.7 on 2025-03-10 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("modules", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="moduleinstance",
            old_name="name",
            new_name="module",
        ),
        migrations.RemoveField(
            model_name="user",
            name="first_name",
        ),
        migrations.RemoveField(
            model_name="user",
            name="last_name",
        ),
        migrations.AddField(
            model_name="professor",
            name="prof_id",
            field=models.CharField(default="", max_length=10),
        ),
        migrations.AddField(
            model_name="user",
            name="username",
            field=models.CharField(default="", max_length=30),
        ),
        migrations.AlterField(
            model_name="module",
            name="code",
            field=models.CharField(default="", max_length=10),
        ),
        migrations.AlterField(
            model_name="module",
            name="name",
            field=models.CharField(default="", max_length=30),
        ),
        migrations.AlterField(
            model_name="moduleinstance",
            name="semester",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="moduleinstance",
            name="year",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="professor",
            name="first_name",
            field=models.CharField(default="", max_length=20),
        ),
        migrations.AlterField(
            model_name="professor",
            name="last_name",
            field=models.CharField(default="", max_length=20),
        ),
        migrations.AlterField(
            model_name="rating",
            name="rating",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(default="", max_length=30),
        ),
        migrations.AlterField(
            model_name="user",
            name="password",
            field=models.CharField(default="", max_length=30),
        ),
    ]
