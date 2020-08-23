from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_TIMEOUT = 100


class Delayer:
    def __init__(self, browser):
        self.browser = browser

    def presence(self, type_by, path, timeout=DEFAULT_TIMEOUT):
        WebDriverWait(self.browser, timeout).until(
            expected_conditions.presence_of_element_located(
                (type_by, path)
            )
        )

    def clickable(self, type_by, path, timeout=DEFAULT_TIMEOUT):
        WebDriverWait(self.browser, timeout).until(
            expected_conditions.element_to_be_clickable(
                (type_by, path)
            )
        )

    def presence_all(self, type_by, path, timeout=DEFAULT_TIMEOUT):
        WebDriverWait(self.browser, timeout).until(
            expected_conditions.presence_of_all_elements_located(
                (type_by, path)
            )
        )

    def visibility(self, type_by, path, timeout=DEFAULT_TIMEOUT):
        WebDriverWait(self.browser, timeout).until(
            expected_conditions.visibility_of_all_elements_located(
                (type_by, path)
            )
        )
