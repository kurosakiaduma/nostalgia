# Generated by Django 4.2.2 on 2023-06-21 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0002_member_last_logged"),
    ]

    operations = [
        migrations.AddField(
            model_name="memberimage",
            name="alt",
            field=models.CharField(default="display-image", max_length=255),
            preserve_default=False,
        ),
    ]
