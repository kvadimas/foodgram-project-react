# Generated by Django 3.2.16 on 2023-09-05 01:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_alter_ingredient_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['name'], 'verbose_name': 'Тег', 'verbose_name_plural': 'Теги'},
        ),
    ]