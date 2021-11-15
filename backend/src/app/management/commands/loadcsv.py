import csv
import os.path

from django.core.management.base import BaseCommand

from app.models import Ingredient


class Command(BaseCommand):
    help = 'Load Ingredient model data from .csv'

    def add_arguments(self, parser):
        parser.add_argument(nargs='+', type=str, dest='args')

    def handle(self, *args, **options):
        filepath = args[0]

        result = os.path.exists(filepath)
        if not result:
            self.stdout.write(self.style.ERROR(f'{filepath} not found.'))
            return

        with open(filepath, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                try:
                    Ingredient.objects.create(
                        name=row[0], measurement_unit=row[1])
                except Exception:
                    pass
        self.stdout.write(self.style.SUCCESS('done.'))
