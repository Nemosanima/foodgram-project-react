import json
import random

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(f'{settings.BASE_DIR}/data/ingredients.json') as json_file:
            data = json.load(json_file)
            for i in range(50):
                index = random.randint(0, 1000)
                db = Ingredient(
                    name=data[index]['name'],
                    measurement_unit=data[index]['measurement_unit']
                )
                db.save()
