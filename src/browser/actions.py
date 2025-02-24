from typing import Callable, ContextManager

from selenium.common.exceptions import (ElementClickInterceptedException,
                                        NoSuchElementException,
                                        TimeoutException)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.logs.log import log


class Actions:

    def __init__(
        self,
        driver
    ) -> None:
        self.driver = driver

    def find_element(self, by: str, value: str, time=10):
        try:
            return WebDriverWait(self.driver, time).until(
                EC.presence_of_element_located((by, value))
            )
        except (TimeoutException, NoSuchElementException) as e:
            log.error(f"Not found element: {value} ({e})")
            return None

    def click_element(self, by, value: str):
        element = self.find_element(by, value)

        if element is None:
            return False

        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((by, value))
            )
            element.click()
            return True

        except ElementClickInterceptedException:
            log.error(f"Click blocked: {value}")
        except Exception as e:
            log.exception(f"Click error: {value} ({e})")

        return False

    def force_click_element(self, by, value):
        while True:
            if self.click_element(by, value):
                break
            else:
                self.driver.refresh_page()
