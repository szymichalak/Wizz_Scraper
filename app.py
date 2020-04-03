import time
from scraper.scraper import Scraper
from results import first_way, return_way
import extra_data.functions as func
import numpy as np


def main(browser_name):
    # origin = "Vienna"  # input("Enter city of departure: ")
    # destination = "Tuzla"  # input("Enter city of arrival: ")
    # while True:
    #     some_or_whole = input("Would you like to scrap some months or a whole year (some / whole)? ")
    #     if some_or_whole == "some":
    #         first_month = input("Enter first month: ")
    #         second_month = input("Enter second month: ")
    #         whole = False
    #         break
    #     elif some_or_whole == "whole":
    #         first_month = None
    #         second_month = None
    #         whole = True
    #         break
    #
    # new_scraper = Scraper(browser_name)
    # print(new_scraper.scrap_prices(origin, destination, whole, first_month, second_month))
    # print("average = ", new_scraper.calculate_average("both"))
    # print(new_scraper.first_way_prices)
    # print(new_scraper.return_prices)
    # new_scraper.close_browser()

    x = func.data_to_numpy(first_way)
    print(x.max())
    print((x.min()))
    print((x.mean()))
    print(x.sum()/len(x))
    itemindex = np.where(x == x.min())
    print(itemindex)
    print(len(x))



if __name__ == "__main__":
    your_browser = "Chrome"  # input("What browser do you have (Chrome / Firefox)? ")
    main(your_browser)
