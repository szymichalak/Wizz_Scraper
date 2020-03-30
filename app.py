import time
from scraper.scraper import Scraper


def main(browser_name):
    origin = "Vienna"  # input("Enter city of departure: ")
    destination = "Tuzla"  # input("Enter city of arrival: ")
    some_or_whole = input("Would you like to scrap some months or a whole year (some / whole)? ")
    if some_or_whole == "some":
        first_month = input("Enter first month: ")
        second_month = input("Enter second month: ")
        whole = False
    else:
        first_month = None
        second_month = None
        whole = True

    new_scraper = Scraper(browser_name)
    new_scraper.scrap_prices(origin, destination, whole, first_month, second_month)
    print(new_scraper.calculate_average("first"))
    new_scraper.print_calendar("first")
    time.sleep(10)
    new_scraper.close_browser()


if __name__ == "__main__":
    your_browser = "Firefox"  # input("What browser do you have (Chrome / Firefox)? ")
    main(your_browser)
