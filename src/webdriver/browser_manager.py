from seleniumwire import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.logger_config import log


class BrowserManager:

    def __init__(self, driver_path, max_retries=3):
        """
        :param local_storage_path: Path to local storage JSON file
        :param max_retries: Max retries if the page fails to load
        """
        self.service = Service(executable_path=driver_path)
        self.options = webdriver.ChromeOptions()
        self.options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.driver.execute_cdp_cmd("Network.enable", {})

        self.max_retries = max_retries

    def open_page(self, url, check_element, by=By.CSS_SELECTOR,):
        log.info(f"Opening: {url}")
        self.driver.get(url)

        if not self._retry_until_loaded(by, check_element):
            log.error("❌ Page failed to load. Exiting.")
            self.close_browser()

            raise Exception("Page load error.")

    def refresh_page(self):
        log.info("🔄 Refreshing...")
        self.driver.refresh()

    def close_browser(self):
        self.driver.quit()
        log.info("🛑 Browser closed.")

    def _retry_until_loaded(self, by, value):  # [TODO] Change method name
        """Reload until the page loads successfully."""
        for attempt in range(self.max_retries):
            log.info(f"🔄 Checking page load ({attempt + 1}/{self.max_retries})...")

            if self._is_element_present(by, value):
                return True

            log.warning("🔁 Reloading page...")

            self.driver.refresh()

        log.error("❌ Page failed to load after retries.")

        return False

    def _is_element_present(self, by, value, timeout=10):
        """Проверяет, загружен ли элемент за указанное время."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            log.info(f"✅ Element found: {value}")
            return True

        except TimeoutException:
            log.warning(f"⚠️ Element not found: {value} (Waited {timeout}s)")
            return False
