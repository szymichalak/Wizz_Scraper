from typing import List
import datetime
from dateutil.relativedelta import *

from models.flightSearch import FlightSearch
from models.postData import PostData


class DataGenerator:
    def __init__(self, adult: int):
        self.data: List[PostData] = []
        self.adult = adult

    def generate(self, source: str, destination: str, first_month: int, last_month: int, start_year: int, generate_return=True):
        if first_month > last_month:
            last_month += 12

        if first_month <= last_month:
            for i in range(last_month-first_month+1):
                if first_month + i > 12:
                    start_year += 1
                    first_month -= 12
                    last_month -= 12

                post_data = PostData()
                start_date = datetime.datetime(start_year, first_month+i, 1)
                finish_date = start_date + relativedelta(months=+1) - datetime.timedelta(days=1)
                flight_search = FlightSearch(source, destination,
                                             start_date.strftime('%Y-%m-%d'), finish_date.strftime('%Y-%m-%d'))
                flight_search.departureStation = source
                flight_search.arrivalStation = destination

                flightList = [flight_search]
                if generate_return:
                    flight_search = FlightSearch(destination, source,
                                                 start_date.strftime('%Y-%m-%d'), finish_date.strftime('%Y-%m-%d'))
                    flightList.append(flight_search)
                post_data.flightList = flightList
                post_data.adultCount = self.adult
                self.data.append(post_data)

        return self.data

    def clear(self):
        self.data = []
