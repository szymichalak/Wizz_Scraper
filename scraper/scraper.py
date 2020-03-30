import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from pathlib import Path

import locators.xpath
from delayer.delayer import Delayer
from extra_data.months import months
from time_converter.time_converter import TimeConverter


class Scraper:
    def __init__(self, browser_name):
        if browser_name == "Firefox":
            driver_path = str(Path().absolute()) + "/scraper/geckodriver"
            self.browser = webdriver.Firefox(executable_path=driver_path)
        elif browser_name == "Chrome":
            driver_path = str(Path().absolute()) + "/scraper/chromedriver"
            self.browser = webdriver.Chrome(driver_path)
        self.delayer = Delayer(self.browser)
        self.converter = TimeConverter()
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

            # calculate next month which we will scrape
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

            time.sleep(15)

            first_way = two_ways_prices[0]
            return_way = two_ways_prices[1]
            options = first_way.find_elements_by_tag_name("li")

            # self.delayer.presence(By.CLASS_NAME, "fare-finder__calendar__days__day__container")
            for i, which_way in enumerate([self.first_way_prices, self.return_prices]):
                options = two_ways_prices[i].find_elements_by_tag_name("li")
                for option in options:
                    try:
                        day = option.find_element_by_tag_name("i").text.zfill(2)
                        p_data = option.find_elements_by_tag_name("p")
                        info = [data.text for data in p_data]
                        if "" in info:
                            info.remove("")
                        if "BEST PRICE" in info:
                            info.remove("BEST PRICE")
                        if info:
                            if info[0] == "NO FLIGHT":
                                which_way.append((selected_value + "-" + day, None))
                            else:
                                value, currency = info[0].split("\n")
                                which_way.append((selected_value + "-" + day, float(value)))
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
            week = [('xxxx-xx-xx', None) for _ in range(7)]
            for day_info in self.first_way_prices:
                week_day = self.converter.str_to_date(day_info[0], "short").weekday()
                week[week_day] = day_info
                if week_day == 6:
                    print(week)
            if week[-1] != self.first_way_prices:
                counter = 0
                for i in range(6, 0, -1):
                    counter += 1
                    if week[i][0] < week[i-1][0]:
                        break
                for k in range(counter):
                    week.pop()
                print(week)
