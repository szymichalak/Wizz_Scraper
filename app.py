import time
from scraper.scraper import Scraper
from extra_data.results import first_way, return_way
import extra_data.functions as func
import numpy as np


def main():
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

    new_scraper = Scraper()
    new_scraper.load_example()
    print("average = ", new_scraper.calculate_average("both"))
    print("max_val = ", new_scraper.get_max_min_val("both", "max"))
    print("min_val = ", new_scraper.get_max_min_val("both", "min"))
    print("max_id = ", new_scraper.get_max_min_id("both", "max"))
    print("min_id = ", new_scraper.get_max_min_id("both", "min"))




if __name__ == "__main__":
    main()
