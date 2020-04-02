import json
import datetime
from pathlib import Path

from time_converter.time_converter import TimeConverter


def check_airports(city_one, city_two):
    with open(f"{str(Path().absolute())}/extra_data/airport_codes.json") as json_file:
        data = json.load(json_file)
    try:
        _ = data[city_one]
        _ = data[city_two]
        return True
    except KeyError:
        return False


def need_update():
    TIMEOUT_DAYS = 30

    with open(f"{str(Path().absolute())}/extra_data/airport_codes.json") as json_file:
        data = json.load(json_file)
    converter = TimeConverter()
    updated = converter.str_to_date(data["updated"], "short")
    now = datetime.datetime.today()

    if (now - updated).days > TIMEOUT_DAYS:
        return True
    else:
        return False
