import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from pathlib import Path

import locators.xpath
from delayer.delayer import Delayer
from extra_data.months import months


class Scraper:
    def __init__(self, browser_name):
        if browser_name == "Firefox":
            driver_path = str(Path().absolute()) + "/scraper/geckodriver"
            self.browser = webdriver.Firefox(executable_path=driver_path)
        elif browser_name == "Chrome":
            driver_path = str(Path().absolute()) + "/scraper/chromedriver"
            self.browser = webdriver.Chrome(driver_path)
        self.delayer = Delayer(self.browser)
        self.url = "https://wizzair.com/en-gb/flights/timetable#/"
        self.browser.get(self.url)
        self.browser.maximize_window()
        self.first_way_prices = []
        self.return_prices = []
        self.current_date = datetime.date.today()

    def close_browser(self):
        self.browser.quit()

    def scrap_prices(self, origin, destination, whole_year, start, stop):
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

        # calculate number of iterations
        if whole_year:
            iterations = 12
        else:
            try:
                start_month = int(months.get(start))
                stop_month = int(months.get(stop))
            except Exception:
                print("Wrong months")
                return False
            if start_month == stop_month:
                iterations = 1
            elif start_month > stop_month:
                iterations = 12 - (start_month - stop_month) + 1
            else:
                iterations = stop_month - start_month + 1

        for month_num in range(iterations):
            # wait for months dropdown
            self.delayer.clickable(By.XPATH, locators.xpath.MONTHS_DROPDOWN)
            select_month = Select(self.browser.find_element_by_xpath(locators.xpath.MONTHS_DROPDOWN))

            # calculate next month which we will scraped
            if whole_year:
                selected_month = self.current_date.month + month_num
            else:
                selected_month = start_month + month_num
            selected_year = self.current_date.year
            if selected_month > 12:
                selected_month -= 12
                selected_year += 1
            selected_value = str(selected_year) + "-" + str(selected_month).zfill(2)
            select_month.select_by_value(selected_value)

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
                            self.first_way_prices.append((day, None))
                        else:
                            value, currency = info[0].split("\n")
                            self.first_way_prices.append((day, float(value)))
                except Exception as e:
                    print(e)
                    #  here add some log
        return True

    def calculate_average(self, way):
        if way == "first":
            if len(self.first_way_prices) == 0:
                return None
            sum_prices = 0
            not_none = 0
            for day_info in self.first_way_prices:
                if day_info[1]:
                    sum_prices += day_info[1]
                    not_none += 1
            return sum_prices / not_none

        elif way == "return":
            if len(self.return_prices) == 0:
                return None
            sum_prices = 0
            not_none = 0
            for day_info in self.return_prices:
                if day_info[1]:
                    sum_prices += day_info[1]
                    not_none += 1
            return sum_prices / not_none

    def print_calendar(self, way):
        if way == "first":
            week = []
            for i, day_info in enumerate(self.first_way_prices):
                week.append(day_info)
                if i % 7 == 0:
                    print(week)
                    week = []
            if week:
                print(week)

        elif way == "return":
            week = []
            for i, day_info in enumerate(self.return_prices):
                week.append(day_info)
                if i % 7 == 0:
                    print(week)
                    week = []
            if week:
                print(week)
