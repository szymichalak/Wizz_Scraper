import time
import datetime
import os
import json
from typing import List, Dict

from selenium import webdriver
from seleniumrequests import Chrome
# from seleniumwire import webdriver  # Import from seleniumwire
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from pathlib import Path
import numpy as np

import extra_data.functions as func
from locators import xpath, class_name, id
from delayer.delayer import Delayer
from extra_data.months import months
from time_converter.time_converter import TimeConverter
from extra_data.results import first_way, return_way


class Scraper:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        # prefs = {"profile.managed_default_content_settings.images": 2}
        # chrome_options.add_experimental_option("prefs", prefs)
        # chrome_options.headless = True
        self.browser = webdriver.Chrome(str(Path().absolute()) + "/scraper/chromedriver", chrome_options=chrome_options)
        self.delayer = Delayer(self.browser)
        self.converter = TimeConverter()
        self.first_way_prices = []
        self.return_prices = []
        self.current_date = datetime.date.today()
        self.browser_opened = False

    def open_browser(self):
        url = "https://wizzair.com/en-gb/flights/timetable#/"
        self.browser.get(url)
        self.browser.maximize_window()
        self.browser_opened = True

    def close_browser(self):
        time.sleep(3)
        self.browser.quit()
        self.browser_opened = False

    # def scrap_prices(self, origin, destination, whole_year, start, stop):
    #     start_time = time.time()
    #
    #     check_cities = func.check_airports(origin, destination)
    #     if not check_cities:
    #         return [False, "Bad cities, try again"]
    #
    #     # need_update = func.need_update()
    #     # if need_update:
    #     #     self.scrap_cities()
    #
    #     # calculate number of iterations
    #     if whole_year:
    #         iterations = 12
    #         start_month = self.current_date.month
    #     else:
    #         try:
    #             start_month = int(months.get(start))
    #             stop_month = int(months.get(stop))
    #         except TypeError:
    #             return [False, "Wrong months"]
    #         if start_month == stop_month:
    #             iterations = 1
    #         elif start_month > stop_month:
    #             iterations = 12 - (start_month - stop_month) + 1
    #         else:
    #             iterations = stop_month - start_month + 1
    #
    #     self.open_browser()
    #
    #     # wait for filling (it doesn't work properly so additional sleep is required)
    #     self.delayer.clickable(By.ID, id.DEPARTURE_INPUT)
    #     time.sleep(1)
    #
    #     # set origin
    #     departure = self.browser.find_element_by_id(id.DEPARTURE_INPUT)
    #     departure.send_keys(origin)
    #     self.delayer.clickable(By.XPATH, xpath.CITY_LABEL)
    #     self.browser.find_element_by_xpath(xpath.CITY_LABEL).click()
    #
    #     # set destination
    #     arrival = self.browser.find_element_by_id(id.ARRIVAL_INPUT)
    #     arrival.send_keys(destination)
    #     self.delayer.clickable(By.XPATH, xpath.CITY_LABEL)
    #     self.browser.find_element_by_xpath(xpath.CITY_LABEL).click()
    #
    #     # click search button
    #     self.browser.find_element_by_xpath(xpath.SEARCH_BUTTON).click()
    #
    #     for month_num in range(iterations):
    #         # wait for months dropdown and click it
    #         self.delayer.presence_all(By.CLASS_NAME, class_name.MONTHS_DROPDOWN)
    #         self.delayer.clickable(By.XPATH, xpath.MONTHS_DROPDOWN_UPPER)
    #         self.delayer.clickable(By.XPATH, xpath.MONTHS_DROPDOWN_LOWER)
    #         select_month_upper = Select(self.browser.find_element_by_xpath(xpath.MONTHS_DROPDOWN_UPPER))
    #         select_month_lower = Select(self.browser.find_element_by_xpath(xpath.MONTHS_DROPDOWN_LOWER))
    #
    #         # calculate next month which we will scrape
    #         selected_month = start_month + month_num
    #         selected_year = self.current_date.year
    #         if selected_month > 12:
    #             selected_month -= 12
    #             selected_year += 1
    #         selected_value = str(selected_year) + "-" + str(selected_month).zfill(2)
    #         select_month_upper.select_by_value(selected_value)
    #         select_month_lower.select_by_value(selected_value)
    #
    #         # wait for calendar and prices
    #         self.delayer.presence(By.CLASS_NAME, class_name.CALENDAR)
    #         two_ways_prices = self.browser.find_elements_by_class_name(class_name.CALENDAR)
    #         elements = []
    #         load_break = 0
    #         while len(elements) < 10 and load_break < 20:
    #             elements = self.browser.find_elements_by_class_name(class_name.PRICE)
    #             time.sleep(0.5)
    #             load_break += 0.5
    #
    #         # print(self.browser.get_cookies())
    #         # request = self.browser.requests[2]
    #         # print(request.method)
    #         # print(request.url)
    #         # print(request.path)
    #         # print(request.querystring)
    #         # print(request.params)
    #         # print(request.headers)
    #         # print(request.body)
    #         # print(request.response)
    #
    #         # iterate over calendars and save information
    #         for i, which_way in enumerate([self.first_way_prices, self.return_prices]):
    #             options = two_ways_prices[i].find_elements_by_tag_name("li")
    #             for option in options:
    #                 try:
    #                     day = option.find_element_by_tag_name("i").text.zfill(2)
    #                     p_data = option.find_elements_by_tag_name("p")
    #                     info = [data.text for data in p_data]
    #                     if "" in info:
    #                         info.remove("")
    #                     if "BEST PRICE" in info:
    #                         info.remove("BEST PRICE")
    #                     if info:
    #                         if info[0] != "NO FLIGHT":
    #                             value, currency = info[0].split("\n")
    #                             which_way.append((selected_value + "-" + day, float(value)))
    #                 except Exception as e:
    #                     print(e)
    #
    #     self.close_browser()
    #     stop_time = time.time()
    #     return [True, f"All data has been scraped within {stop_time - start_time} s"]
    #
    # def calculate_average(self, way):
    #     first_copy = self.first_way_prices.copy()
    #     return_copy = self.return_prices.copy()
    #     if way == "first":
    #         active_list = [first_copy]
    #     elif way == "return":
    #         active_list = [return_copy]
    #     elif way == "both":
    #         active_list = [first_copy, return_copy]
    #     else:
    #         return [False, "Wrong way, select: first, return or both"]
    #
    #     result = []
    #     for active in active_list:
    #         if len(active) == 0:
    #             return [False, "No scraped information"]
    #         numpy_array_prices = func.data_to_numpy(active)
    #         result.append(numpy_array_prices.mean())
    #     return result

    def scrap_cities(self, from_routes=False) -> (List, dict):
        if not self.browser_opened:
            self.open_browser()

        # click on input field to open the list of cities
        self.delayer.clickable(By.ID, id.DEPARTURE_INPUT)
        if not from_routes:
            self.browser.find_element_by_id(id.DEPARTURE_INPUT).click()

        self.delayer.presence_all(By.CLASS_NAME, class_name.COUNTY_CONTAINER)
        full_list = self.browser.find_elements_by_class_name(class_name.COUNTY_CONTAINER)
        full_list.pop(0)  # remove closest airports

        cities_dict: Dict[str, tuple] = {}
        countries = []

        for country in full_list:
            self.browser.execute_script("arguments[0].scrollIntoView();", country)

            self.delayer.presence_all(By.CLASS_NAME, class_name.COUNTRY_NAME)
            country_name = country.find_element_by_class_name(class_name.COUNTRY_NAME).text.lower()
            countries.append(country_name)

            cities = country.find_elements_by_tag_name("label")
            cities_list = []
            for city in cities:
                city_name = city.find_element_by_tag_name("strong").text
                airport_code = city.find_element_by_tag_name("small").text
                cities_list.append((city_name, airport_code, country_name))
            cities_dict[country_name] = cities_list

        self.close_browser()
        return countries, cities_dict

        # # create a folder
        # countries_path = str(Path().absolute()) + "/countries"
        # if not Path(countries_path).exists():
        #     os.mkdir(countries_path, 0o755)
        #
        # # create files with available cities
        # for single_country in data:
        #     with open(f"{countries_path}/{single_country}.txt", "w") as file:
        #         for item in data[single_country]:
        #             file.write("%s\n" % item[0])
        #
        # # create a .json file with all airports codes (city: code)
        # dir_to_json = {"updated": self.converter.date_to_str(datetime.date.today(), "short")}
        # for single_country in data:
        #     for single_city in data[single_country]:
        #         dir_to_json[single_city[0]] = single_city[1]
        # with open(f"{str(Path().absolute())}/extra_data/airport_codes.json", "w") as f:
        #     json.dump(dir_to_json, f)

    def scrap_routes(self, airport_code) -> (List, dict):
        if not self.browser_opened:
            self.open_browser()

        # wait for filling (it doesn't work properly so additional sleep is required)
        self.delayer.clickable(By.ID, id.DEPARTURE_INPUT)
        time.sleep(1)

        # set origin
        departure = self.browser.find_element_by_id(id.DEPARTURE_INPUT)
        departure.send_keys(airport_code)
        self.delayer.clickable(By.XPATH, xpath.CITY_LABEL)
        self.browser.find_element_by_xpath(xpath.CITY_LABEL).click()

        # set fake destination to show list
        arrival = self.browser.find_element_by_id(id.ARRIVAL_INPUT)
        arrival.send_keys('')

        return self.scrap_cities(from_routes=True)

    # def split_to_months(self, way):
    #     first_copy = self.first_way_prices.copy()
    #     return_copy = self.return_prices.copy()
    #     if way == "first":
    #         active_list = [first_copy]
    #     elif way == "return":
    #         active_list = [return_copy]
    #     elif way == "both":
    #         active_list = [first_copy, return_copy]
    #     else:
    #         return [False, "Wrong way, select: first, return or both"]
    #
    #     result = []
    #     for active in active_list:
    #         year = []
    #         current = active[0][0][5:7]
    #         month = []
    #         for data in active:
    #             if data[0][5:7] != current:
    #                 year.append(month)
    #                 current = data[0][5:7]
    #                 month = [data]
    #             else:
    #                 month.append(data)
    #         year.append(month)
    #         result.append(year)
    #     return result
    #
    # def get_max_min_id(self, way, max_or_min):
    #     first_copy = self.first_way_prices.copy()
    #     return_copy = self.return_prices.copy()
    #     if way == "first":
    #         active_list = [first_copy]
    #     elif way == "return":
    #         active_list = [return_copy]
    #     elif way == "both":
    #         active_list = [first_copy, return_copy]
    #     else:
    #         return [False, "Wrong way, select: first, return or both"]
    #
    #     result = []
    #     for active in active_list:
    #         if len(active) == 0:
    #             return [False, "No scraped information"]
    #         numpy_array_prices = func.data_to_numpy(active)
    #         if max_or_min == "max":
    #             items_id = np.where(numpy_array_prices == numpy_array_prices.max())
    #         elif max_or_min == "min":
    #             items_id = np.where(numpy_array_prices == numpy_array_prices.min())
    #         else:
    #             return [False, "Bad argument, take max or min "]
    #         result.append(items_id[0])
    #     return result
    #
    # def get_max_min_val(self, way, max_or_min):
    #     first_copy = self.first_way_prices.copy()
    #     return_copy = self.return_prices.copy()
    #     if way == "first":
    #         active_list = [first_copy]
    #     elif way == "return":
    #         active_list = [return_copy]
    #     elif way == "both":
    #         active_list = [first_copy, return_copy]
    #     else:
    #         return [False, "Wrong way, select: first, return or both"]
    #
    #     result = []
    #     for active in active_list:
    #         if len(active) == 0:
    #             return [False, "No scraped information"]
    #         numpy_array_prices = func.data_to_numpy(active)
    #         if max_or_min == "max":
    #             value = numpy_array_prices.max()
    #         elif max_or_min == "min":
    #             value = numpy_array_prices.min()
    #         else:
    #             return [False, "Bad argument, take max or min "]
    #         result.append(value)
    #     return result
    #
    # def load_example(self):
    #     self.first_way_prices = first_way
    #     self.return_prices = return_way
