import csv
from app.models import Ingredient

filename = '../data/ingredients.csv'
# это решение мне не нравиться, думаю чем заменить :]


def load():
    with open(filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            try:
                Ingredient.objects.create(name=row[0], measurement_unit=row[1])
            except Exception:
                pass
    print('done.')
