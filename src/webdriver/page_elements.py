from selenium.common.exceptions import (ElementClickInterceptedException,
                                        NoSuchElementException,
                                        TimeoutException)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.logger_config import log


class PageElements:

    def __init__(self, driver) -> None:
        self.driver = driver

    def find_element(self, by: str, value: str, time=10):
        try:
            return WebDriverWait(self.driver, time).until(
                EC.presence_of_element_located((by, value))
            )
        except (TimeoutException, NoSuchElementException) as e:
            log.warning(f"⚠️ Not found element: {value} ({e})")
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
            log.info(f"🖱️ Clicked: {value}")
            return True

        except ElementClickInterceptedException:
            log.error(f"❌ Click blocked: {value}")
        except Exception as e:
            log.error(f"❌ Click error: {value} ({e})", exc_info=True)

        return False

    def force_click_element(self, by, value):
        while True:
            if self.click_element(by, value):
                log.info("✅ Click successful.")
                break
            else:
                self.driver.refresh_page()
                log.warning("⚠️ Click failed. Retrying...")
