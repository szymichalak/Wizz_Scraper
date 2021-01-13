from typing import List
from models.flightSearch import FlightSearch


class PostData:
    def __init__(self):
        self.flightList: List[FlightSearch] = []
        self.priceType: str = "regular"
        self.adultCount: int = 0
        self.childCount: int = 0
        self.infantCount: int = 0

    def to_dictionary(self):
        flightList = []
        for flight_search in self.flightList:
            flightList.append(flight_search.to_dictionary())
        return {
            "flightList": flightList,
            "priceType": self.priceType,
            "adultCount": self.adultCount,
            "childCount": self.childCount,
            "infantCount": self.infantCount
        }
