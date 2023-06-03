import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(f'{settings.BASE_DIR}/data/ingredients.csv') as csv_file:
            file_reader = csv.DictReader(csv_file)
            for row in file_reader:
                db = Ingredient(
                    name=row['name'],
                    measurement_unit=row['measurement_unit']
                )
                db.save()
