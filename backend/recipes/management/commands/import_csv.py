import csv

from django.core.management.base import BaseCommand

from essences.models import Ingredient


class Command(BaseCommand):
    help = 'Заполнение таблицы ингредиентов из csv-файла'

    def handle(self, *args, **kwargs):
        self.stdout.write('Загрузка запущена...')
        Ingredient.objects.all().delete()
        with open('ingredients.csv') as csv_file:
            csv_reader = csv.DictReader(
                csv_file, fieldnames=['name', 'measurement_unit'],
                delimiter=',')
            line_count = 0
            for row in csv_reader:
                ingredient = Ingredient(
                    name=row['name'], measurement_unit=row['measurement_unit'])
                ingredient.save()
                line_count += 1
        self.stdout.write('Добавлено строк %s' % line_count)
