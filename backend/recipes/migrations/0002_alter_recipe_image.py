# Generated by Django 3.2.3 on 2023-08-04 08:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="recipes/images/",
                verbose_name="Ссылка на картинку на сайте",
            ),
        ),
    ]