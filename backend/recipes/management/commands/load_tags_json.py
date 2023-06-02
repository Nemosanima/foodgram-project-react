import json

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(f'{settings.BASE_DIR}/data/tags.json') as json_file:
            data = json.load(json_file)
            for i in data:
                db = Tag(
                    name=i['name'],
                    color=i['color'],
                    slug=i['slug']
                )
                db.save()
