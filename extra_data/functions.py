import json
import datetime
from pathlib import Path
import numpy as np

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


def data_to_numpy(data_list):
    for i in range(len(data_list)):
        data_list[i] = data_list[i][1]
    return np.asarray(data_list, dtype=np.float32)


def split_data(data_list):
    dates = []
    prices = []
    for info in data_list:
        dates.append(info[0])
        prices.append(info[1])
    return dates, prices


def split_to_months(year_data):
    year = []
    current = year_data[0][5:7]
    month = []
    for data in year_data:
        if data[0][5:7] != current:
            year.append(month)
            current = data[0][5:7]
            month = [data]
        else:
            month.append(data)
    year.append(month)
    return year
