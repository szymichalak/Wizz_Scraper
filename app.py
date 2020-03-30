import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

import locators.xpath
from delayer.delayer import Delayer
from extra_data.months import months


class Scraper:
    def __init__(self, driver_path):
        self.url = "https://wizzair.com/en-gb/flights/timetable#/"
        self.browser = webdriver.Firefox(executable_path=driver_path)
        self.delayer = Delayer(self.browser)
        self.browser.get(self.url)

    def close_browser(self):
        self.browser.quit()

    def scrap_some_months(self, origin, destination, start, stop):
        # wait for filling
        self.delayer.clickable(By.ID, "search-departure-station")

        # set origin
        departure = self.browser.find_element_by_id("search-departure-station")
        time.sleep(0.5)
        departure.send_keys(origin)
        self.delayer.clickable(By.XPATH, locators.xpath.CITY_LABEL)
        self.browser.find_element_by_xpath(locators.xpath.CITY_LABEL).click()

        # set destination
        arrival = self.browser.find_element_by_id("search-arrival-station")
        arrival.send_keys(destination)
        self.delayer.clickable(By.XPATH, locators.xpath.CITY_LABEL)
        self.browser.find_element_by_xpath(locators.xpath.CITY_LABEL).click()

        # click search button
        self.browser.find_element_by_xpath(locators.xpath.SEARCH_BUTTON).click()

        result_prices = []
        start_month = int(months.get(start))
        stop_month = int(months.get(stop)) + 1
        for month_num in range(start_month, stop_month):
            self.delayer.clickable(By.XPATH, locators.xpath.MONTHS_DROPDOWN)
            select_month = Select(self.browser.find_element_by_xpath(locators.xpath.MONTHS_DROPDOWN))
            select_month.select_by_value("2020-0" + str(month_num))

            self.delayer.presence(By.CLASS_NAME, "fare-finder__calendar__days__list")
            two_ways_prices = self.browser.find_elements_by_class_name("fare-finder__calendar__days__list")

            first_way = two_ways_prices[0]
            options = first_way.find_elements_by_tag_name("li")
            time.sleep(15)
            # self.delayer.presence(By.CLASS_NAME, "fare-finder__calendar__days__day__container")
            for option in options:
                try:
                    day = int(option.find_element_by_tag_name("i").text)
                    p_data = option.find_elements_by_tag_name("p")
                    info = [data.text for data in p_data]
                    if "" in info:
                        info.remove("")
                    if "BEST PRICE" in info:
                        info.remove("BEST PRICE")
                    if info:
                        if info[0] == "NO FLIGHT":
                            result_prices.append((day, info[0]))
                        else:
                            value, currency = info[0].split("\n")
                            result_prices.append((day, float(value)))
                except Exception as e:
                    print(e)
                    #  here add some log

        for information in result_prices:
            print(information)


webdriver_path = '/home/szymon/PycharmProjects/Wizz_Scraper/geckodriver'
new_scraper = Scraper(webdriver_path)
new_scraper.scrap_some_months("Vienna", "Tuzla", "May", "July")
time.sleep(10)
new_scraper.close_browser()
