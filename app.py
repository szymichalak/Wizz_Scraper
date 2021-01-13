# import time
# from scraper.scraper import Scraper
# from extra_data.results import first_way, return_way
# import extra_data.functions as func
# import numpy as np
# from plotter.plotter import Plotter
#
#
# def main():
#     origin = "Vienna"  # input("Enter city of departure: ")
#     destination = "Tuzla"  # input("Enter city of arrival: ")
#     while True:
#         some_or_whole = input("Would you like to scrap some months or a whole year (some / whole)? ")
#         if some_or_whole == "some":
#             first_month = input("Enter first month: ")
#             second_month = input("Enter second month: ")
#             whole = False
#             break
#         elif some_or_whole == "whole":
#             first_month = None
#             second_month = None
#             whole = True
#             break
#
#     # new_scraper = Scraper()
#     # new_scraper.load_example()
#
#     new_scraper = Scraper()
#     new_scraper.scrap_prices(origin, destination, whole, first_month, second_month)
#
#
#     # print("average = ", new_scraper.calculate_average("both"))
#     # print("max_val = ", new_scraper.get_max_min_val("both", "max"))
#     # print("min_val = ", new_scraper.get_max_min_val("both", "min"))
#     # print("max_id = ", new_scraper.get_max_min_id("both", "max"))
#     # print("min_id = ", new_scraper.get_max_min_id("both", "min"))
#
#     # new_plotter = Plotter(True, True)
#     # new_plotter.create_plot(return_way)
#
#
#
#
#
# if __name__ == "__main__":
#     main()
from models.flightSearch import FlightSearch
from wizz_request.dataGenerator import DataGenerator
from wizz_request.wizz_request import WizzRequest

data_07 = {
    "flightList":
        [
            {
                "departureStation": "TIA",
                "arrivalStation": "VIE",
                "from": "2021-07-10",
                "to": "2021-07-20"
            },
            {
                "departureStation": "VIE",
                "arrivalStation": "TIA",
                "from": "2021-07-10",
                "to": "2021-07-20"
            }
        ],
    "priceType": "regular",
    "adultCount": 1,
    "childCount": 0,
    "infantCount": 0
}

# wizz_req = WizzRequest()
# wizz_req.make_request(data_07)
# wizz_req.parse_response()

data_gen = DataGenerator(1)
x = data_gen.generate('ViA', 'TIA', 7, 5, 2020)
for q in x:
    print(q.to_dictionary())
