import time
from scraper.scraper import Scraper


def main(browser_name):
    origin = input("Enter city of departure: ")
    destination = input("Enter city of arrival: ")
    new_scraper = Scraper(browser_name)
    new_scraper.scrap_some_months(origin, destination, "May", "July")
    print(new_scraper.calculate_average("first"))
    new_scraper.print_calendar("first")
    time.sleep(10)
    new_scraper.close_browser()


if __name__ == "__main__":
    your_browser = input("What browser do you have (Chrome / Firefox)? ")
    main(your_browser)
