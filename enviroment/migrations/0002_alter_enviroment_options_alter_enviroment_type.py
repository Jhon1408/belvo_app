# Generated by Django 4.1.7 on 2023-03-01 08:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("enviroment", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="enviroment",
            options={
                "ordering": ["-created_at"],
                "verbose_name": "Enviroment Variable",
                "verbose_name_plural": "Enviroment Variables",
            },
        ),
        migrations.AlterField(
            model_name="enviroment",
            name="type",
            field=models.CharField(
                choices=[
                    ("string", "string"),
                    ("int", "int"),
                    ("float", "float"),
                    ("bool", "bool"),
                ],
                max_length=255,
            ),
        ),
    ]
