import csv

from django.apps import apps
from django.core.management.base import BaseCommand


class MyBaseCommand(BaseCommand):
    def add_arguments(self, parser):
        """Использование опционального не обязательного аргумента"""
        parser.add_argument(
            "-d",
            "--delite",
            action="store_true",
            dest="delete_existing",
            default=False,
            help="Удалить существующие записи в таблице перед созданием новых",
        )
        parser.add_argument(
            "-p",
            "--path",
            dest="file_path",
            type=str,
            help=(
                "Добавьте путь до файла импорта по типу ",
                "<recipes/data/ingredients.csv>",
            ),
        )
        parser.add_argument(
            "-t",
            "--table_import",
            action="append",
            dest="table_import",
            type=str,
            help=(
                "Добавьте в строгой последовательности имя приложения ",
                "и имя Модели по типу <recipes Ingredient>",
            ),
        )


class Command(MyBaseCommand):
    help = "Импонтировать данные из csv"

    def handle(self, *args, **options):
        """Метод импортирующий csv в базу данных"""
        try:
            _name = "Ingredient"
            _app = "recipes"
            _model = apps.get_model(_app, _name)
        except:
            self.stdout.write(
                self.style.WARNING(
                    "Ошибка при добавлении аргументов импорта модели"
                )
            )
            return

        if options["delete_existing"]:
            _model.objects.all().delete()
            self.stdout.write(
                self.style.WARNING(
                    f"Таблица {_name} очищена от старых записей."
                )
            )

        if options["file_path"]:
            link = options("file_path")
        else:
            link = "recipes/data/ingredients.csv"

        # Подсчет добавляемых строк
        with open(link, encoding="utf-8") as csvfile:
            count_row = len(list(csv.DictReader(csvfile)))

            # Запись
            with open(link, encoding="utf-8") as csvfile:
                dict_reader = csv.DictReader(
                    csvfile, fieldnames=("name", "measurement_unit")
                )
                for i in dict_reader:
                    _model.objects.get_or_create(**i)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Добавлено {count_row} записей в таблицу {_name}."
                    )
                )
