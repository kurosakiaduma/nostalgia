# Generated by Django 4.2.2 on 2023-06-18 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0004_alter_member_birth_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="member",
            name="last_login",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="last login"
            ),
        ),
    ]