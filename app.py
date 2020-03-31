import time
from scraper.scraper import Scraper


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
    # new_scraper.scrap_prices(origin, destination, whole, first_month, second_month)
    # print("average = ", new_scraper.calculate_average("both"))
    # new_scraper.close_browser()
    new_scraper = Scraper(browser_name)
    new_scraper.open_browser(3)


if __name__ == "__main__":
    your_browser = "Firefox"  # input("What browser do you have (Chrome / Firefox)? ")
    main(your_browser)
