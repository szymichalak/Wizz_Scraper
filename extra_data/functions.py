import json
from pathlib import Path


def check_airports(self, city_one, city_two):
    with open(f"{str(Path().absolute())}/extra_data/airport_codes.json") as json_file:
        data = json.load(json_file)
    if city_one and city_two in data:
        return True
    else:
        return False
