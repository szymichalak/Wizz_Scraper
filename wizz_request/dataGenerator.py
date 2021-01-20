import copy
from typing import List
from datetime import datetime, timedelta

from models.postData import PostData


def last_day_of_next_month(date: datetime):
    year = date.year
    month = date.month
    if month + 1 > 12:
        year += 1
        month -= 11
        new_date = datetime(year, month + 1, 1)
    elif month + 2 > 12:
        year += 1
        month -= 11
        new_date = datetime(year, month + 1, 1)
    else:
        new_date = datetime(year, month + 2, 1)
    return new_date - timedelta(days=1)


class DataGenerator:
    def __init__(self, input_data: PostData):
        self.__input_data = input_data
        self.__data: List[PostData] = []
        self.__format = '%Y-%m-%d'
        self.__start_date: datetime
        self.__end_date: datetime
        self.__months: int
        if len(self.__input_data.flightList) > 0:
            self.__start_date = datetime.strptime(self.__input_data.flightList[0].from_date, self.__format)
            self.__end_date = datetime.strptime(self.__input_data.flightList[0].to_date, self.__format)

            if self.__start_date.year == self.__end_date.year and self.__start_date.month == self.__end_date.month:
                self.__months = 1
            else:
                self.__months = (self.__end_date.year - self.__start_date.year) * 12 + \
                              (self.__end_date.month - self.__start_date.month) + 1

    def generate(self):
        self.clear()

        if self.__months == 1:
            self.__data.append(self.__input_data)
        else:
            first = copy.deepcopy(self.__input_data)
            for flight in first.flightList:
                flight.from_date = datetime(self.__start_date.year, self.__start_date.month, self.__start_date.day)
                flight.to_date = datetime(self.__start_date.year, self.__start_date.month + 1, 1) - timedelta(days=1)
            self.__data.append(first)

            next_month = copy.deepcopy(first)
            for i in range(self.__months - 2):
                for j, flight in enumerate(next_month.flightList):
                    flight.from_date = next_month.flightList[j].to_date + timedelta(days=1)
                    flight.to_date = last_day_of_next_month(next_month.flightList[j].to_date)
                self.__data.append(copy.deepcopy(next_month))
                next_month = copy.deepcopy(next_month)

            last_month = copy.deepcopy(next_month)
            for i, flight in enumerate(last_month.flightList):
                flight.from_date = last_month.flightList[i].to_date + timedelta(days=1)
                flight.to_date = self.__end_date
            self.__data.append(copy.deepcopy(last_month))
        return self.__data

    def clear(self):
        self.__data = []
