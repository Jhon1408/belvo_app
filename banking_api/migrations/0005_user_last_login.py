# Generated by Django 4.1.7 on 2023-03-01 18:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("banking_api", "0004_auth_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="last_login",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
