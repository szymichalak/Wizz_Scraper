import time
import datetime
import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from pathlib import Path

import extra_data.functions as func
from locators import xpath, class_name, id
from delayer.delayer import Delayer
from extra_data.months import months
from time_converter.time_converter import TimeConverter


class Scraper:
    def __init__(self, browser_name):
        if browser_name == "Firefox":
            firefox_profile = webdriver.FirefoxProfile()
            # firefox_profile.set_preference('permissions.default.image', 2)
            # firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
            firefox_options = webdriver.FirefoxOptions()
            # firefox_options.headless = True
            driver_path = str(Path().absolute()) + "/scraper/geckodriver"
            self.browser = webdriver.Firefox(executable_path=driver_path,
                                             firefox_profile=firefox_profile, firefox_options=firefox_options)
        elif browser_name == "Chrome":
            chrome_options = webdriver.ChromeOptions()
            # prefs = {"profile.managed_default_content_settings.images": 2}
            # chrome_options.add_experimental_option("prefs", prefs)
            # chrome_options.headless = True
            driver_path = str(Path().absolute()) + "/scraper/chromedriver"
            self.browser = webdriver.Chrome(driver_path, chrome_options=chrome_options)
        self.delayer = Delayer(self.browser)
        self.converter = TimeConverter()
        self.first_way_prices = []
        self.return_prices = []
        self.current_date = datetime.date.today()

    def open_browser(self, tabs):
        # self.browser.maximize_window()
        # self.browser.minimize_window()
        for tab_num in range(1, tabs+1):
            url = "https://wizzair.com/en-gb/flights/timetable#/"
            self.browser.get(url)
            if tab_num < tabs:
                self.browser.execute_script("window.open('about:blank');")
                self.browser.switch_to.window(self.browser.window_handles[tab_num])

    def close_browser(self):
        self.browser.quit()

    def scrap_prices(self, origin, destination, whole_year, start, stop):
        start_time = time.time()
        print("start")

        need_update = func.need_update()
        if need_update:
            self.scrap_cities()

        # calculate number of iterations and tabs
        if whole_year:
            iterations = 12
            start_month = self.current_date.month
        else:
            try:
                start_month = int(months.get(start))
                stop_month = int(months.get(stop))
            except TypeError:
                return [False, "Wrong months"]
            if start_month == stop_month:
                iterations = 1
            elif start_month > stop_month:
                iterations = 12 - (start_month - stop_month) + 1
            else:
                iterations = stop_month - start_month + 1

        self.open_browser(1)

        # wait for filling (it doesn't work properly so additional sleep is required)
        self.delayer.clickable(By.ID, id.DEPARTURE_INPUT)
        time.sleep(1)

        # set origin
        departure = self.browser.find_element_by_id(id.DEPARTURE_INPUT)
        departure.send_keys(origin)
        self.delayer.clickable(By.XPATH, xpath.CITY_LABEL)
        self.browser.find_element_by_xpath(xpath.CITY_LABEL).click()

        # set destination
        arrival = self.browser.find_element_by_id(id.ARRIVAL_INPUT)
        arrival.send_keys(destination)
        self.delayer.clickable(By.XPATH, xpath.CITY_LABEL)
        self.browser.find_element_by_xpath(xpath.CITY_LABEL).click()

        # click search button
        self.browser.find_element_by_xpath(xpath.SEARCH_BUTTON).click()

        for month_num in range(iterations):
            # wait for months dropdown and click it
            self.delayer.presence_all(By.CLASS_NAME, class_name.MONTHS_DROPDOWN)
            self.delayer.clickable(By.XPATH, xpath.MONTHS_DROPDOWN_UPPER)
            self.delayer.clickable(By.XPATH, xpath.MONTHS_DROPDOWN_LOWER)
            select_month_upper = Select(self.browser.find_element_by_xpath(xpath.MONTHS_DROPDOWN_UPPER))
            select_month_lower = Select(self.browser.find_element_by_xpath(xpath.MONTHS_DROPDOWN_LOWER))

            # calculate next month which we will scrape
            selected_month = start_month + month_num
            selected_year = self.current_date.year
            if selected_month > 12:
                selected_month -= 12
                selected_year += 1
            selected_value = str(selected_year) + "-" + str(selected_month).zfill(2)
            select_month_upper.select_by_value(selected_value)
            select_month_lower.select_by_value(selected_value)

            # wait for calendar and prices
            self.delayer.presence(By.CLASS_NAME, class_name.CALENDAR)
            two_ways_prices = self.browser.find_elements_by_class_name(class_name.CALENDAR)
            elements = []
            load_break = 0
            while len(elements) < 10 and load_break < 20:
                elements = self.browser.find_elements_by_class_name(class_name.PRICE)
                time.sleep(0.5)
                load_break += 0.5

            # iterate over calendars and save information
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
                            if info[0] != "NO FLIGHT":
                                value, currency = info[0].split("\n")
                                which_way.append((selected_value + "-" + day, float(value)))
                    except Exception as e:
                        print(e)

        stop_time = time.time()
        return [True, f"All data has been scraped within {stop_time - start_time} s"]

    def calculate_average(self, way):
        if way == "first":
            active_list = [self.first_way_prices]
        elif way == "return":
            active_list = [self.return_prices]
        elif way == "both":
            active_list = [self.first_way_prices, self.return_prices]
        else:
            return [False, "Wrong way, select: first, return or both"]

        result = []
        for active in active_list:
            if len(active) == 0:
                return [False, "No scraped information"]
            numpy_array_prices = func.data_to_numpy(active)
            result.append(numpy_array_prices.mean())
        return result

    def scrap_cities(self):
        self.open_browser(1)

        # click on input field to open the list of cities
        self.delayer.clickable(By.ID, id.DEPARTURE_INPUT)
        self.browser.find_element_by_id(id.DEPARTURE_INPUT).click()

        self.delayer.presence_all(By.CLASS_NAME, class_name.COUNTY_CONTAINER)
        full_list = self.browser.find_elements_by_class_name(class_name.COUNTY_CONTAINER)

        # store data in dictionary and save it into a files
        data = {}
        for country in full_list:
            self.browser.execute_script("arguments[0].scrollIntoView();", country)
            self.delayer.presence_all(By.CLASS_NAME, class_name.COUNTRY_NAME)
            country_name = country.find_element_by_class_name(class_name.COUNTRY_NAME).text.lower()
            cities = country.find_elements_by_tag_name("label")
            cities_list = []
            for city in cities:
                city_name = city.find_element_by_tag_name("strong").text
                city_code = city.find_element_by_tag_name("small").text
                cities_list.append((city_name, city_code))
            data[country_name] = cities_list

        self.close_browser()

        # create a folder
        countries_path = str(Path().absolute()) + "/countries"
        if not Path(countries_path).exists():
            os.mkdir(countries_path, 0o755)

        # create files with available cities
        for single_country in data:
            with open(f"{countries_path}/{single_country}.txt", "w") as file:
                for item in data[single_country]:
                    file.write("%s\n" % item[0])

        # create a .json file with all airports codes (city: code)
        dir_to_json = {"updated": self.converter.date_to_str(datetime.date.today(), "short")}
        for single_country in data:
            for single_city in data[single_country]:
                dir_to_json[single_city[0]] = single_city[1]
        with open(f"{str(Path().absolute())}/extra_data/airport_codes.json", "w") as f:
            json.dump(dir_to_json, f)
