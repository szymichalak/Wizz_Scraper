import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

import locators.xpath
from delayer.delayer import Delayer


browser = webdriver.Firefox(executable_path='/home/szymon/PycharmProjects/Wizz_Scraper/geckodriver')

url = "https://wizzair.com/en-gb/flights/timetable#/"
browser.get(url)

# create delayer
delayer = Delayer(browser)

# set origin
delayer.presence(By.ID, "search-departure-station")

departure = browser.find_element_by_id("search-departure-station")
time.sleep(0.5)
departure.send_keys("Vienna")
delayer.presence(By.XPATH, locators.xpath.CITY_LABEL)
dep_click = browser.find_element_by_xpath(locators.xpath.CITY_LABEL)
dep_click.click()

# set destination
arrival = browser.find_element_by_id("search-arrival-station")
time.sleep(0.5)
arrival.send_keys("Tuzla")
delayer.presence(By.XPATH, locators.xpath.CITY_LABEL)
arr_click = browser.find_element_by_xpath(locators.xpath.CITY_LABEL)
arr_click.click()

# click search button
search_button = browser.find_element_by_xpath(locators.xpath.SEARCH_BUTTON)
search_button.click()


result_prices = []

for month_num in range(6, 7):
    delayer.clickable(By.XPATH, locators.xpath.MONTHS_DROPDOWN)
    select_month = Select(browser.find_element_by_xpath(locators.xpath.MONTHS_DROPDOWN))
    select_month.select_by_value("2020-0"+str(month_num))

    delayer.presence(By.CLASS_NAME, "fare-finder__calendar__days__list")
    months_lists = browser.find_elements_by_class_name("fare-finder__calendar__days__list")

    options = months_lists[0].find_elements_by_tag_name("li")
    time.sleep(15)
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
                result_prices.append((day, info))
        except Exception as e:
            print(e)


browser.quit()

for information in result_prices:
    print(information)

