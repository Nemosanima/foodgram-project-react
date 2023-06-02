import json

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(f'{settings.BASE_DIR}/data/ingredients.json') as json_file:
            data = json.load(json_file)
            for i in range(50):
                db = Ingredient(
                    name=data[i]['name'],
                    measurement_unit=data[i]['measurement_unit']
                )
                db.save()
