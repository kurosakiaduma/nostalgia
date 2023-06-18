# Generated by Django 4.2.2 on 2023-06-18 09:39

import backend.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="member",
            name="child_of",
        ),
        migrations.RemoveField(
            model_name="member",
            name="is_founder",
        ),
        migrations.AddField(
            model_name="member",
            name="father",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="children_father",
                to="backend.member",
            ),
        ),
        migrations.AddField(
            model_name="member",
            name="mother",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="children_mother",
                to="backend.member",
            ),
        ),
        migrations.AlterField(
            model_name="memberimage",
            name="image",
            field=models.ImageField(upload_to=backend.models.get_upload_path),
        ),
        migrations.CreateModel(
            name="Story",
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
                ("title", models.CharField(max_length=255)),
                ("content", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="backend.member"
                    ),
                ),
                (
                    "family",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="backend.family"
                    ),
                ),
            ],
        ),
    ]