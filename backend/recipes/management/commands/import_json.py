import json

from django.apps import apps
from recipes.management.commands.import_csv import MyBaseCommand


class Command(MyBaseCommand):
    help = "Импонтировать данные из json"

    def handle(self, *args, **options):
        """Метод импортирующий json в базу данных"""
        try:
            _name = "Ingredient"
            _app = "recipes"
            _model = apps.get_model(_app, _name)
        except:
            self.stdout.write(
                self.style.WARNING("Ошибка при добавлении аргументов импорта модели")
            )
            return

        if options["delete_existing"]:
            _model.objects.all().delete()
            self.stdout.write(
                self.style.WARNING(f"Таблица {_name} очищена от старых записей.")
            )

        if options["file_path"]:
            link = options("file_path")
        else:
            link = "recipes/data/ingredients.json"

        # Подсчет добавляемых строк
        with open(link, encoding="utf-8") as jsonfile:
            count_row = len(json.load(jsonfile))

            with open(link, encoding="utf-8") as jsonfile:
                dict_reader = json.load(jsonfile)
                for i in dict_reader:
                    _model.objects.get_or_create(
                        name=i["name"], measurement_unit=i["measurement_unit"]
                    )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Добавлено {count_row} записей в таблицу {_name}."
                    )
                )
