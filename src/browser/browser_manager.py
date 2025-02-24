from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from seleniumwire import webdriver

from src.config import config
from src.logs.log import log


class BrowserManager:

    def __init__(
        self,
        driver_path,
    ):
        """
        :param driver_path: WebDriver path
        """
        super().__init__()
        self.service = Service(executable_path=driver_path)

        self.options = webdriver.ChromeOptions()
        self.options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

        if config.headless_mode:
            self.options.add_argument("--headless")

        # Seleniumwire settings
        self.seleniumwire_options = {}

        if config.use_proxy:
            self._set_proxy()

        self.driver = webdriver.Chrome(
            service=self.service,
            options=self.options,
            seleniumwire_options=self.seleniumwire_options,
        )
        self.driver.execute_cdp_cmd("Network.enable", {})

        self.driver.request_interceptor = self._modify_headers

    def open_page(self, url, check_element, by=By.CSS_SELECTOR):
        log.info(f"Try to open: {url}")
        self.driver.get(url)

        if not self._retry_until_loaded(by, check_element):
            self.close_browser()

            raise Exception("Page load error.")

    def refresh_page(self):
        log.info("Refresh page")
        self.driver.refresh()

    def close_browser(self):
        self.driver.quit()

    def _retry_until_loaded(
        self, by, value, max_retries=3
    ):  # [TODO] Change method name
        """
        Reload until the page loads successfully.

        :param max_retries: Max retries if the page fails to load
        """
        for attempt in range(max_retries):
            log.info(f"Checking page load: attempt ({attempt + 1}/{max_retries})")

            if self._is_element_present(by, value):
                return True

            self.driver.refresh()

        log.error(f"Page failed to load after retries")

        return False

    def _is_element_present(self, by, value, timeout=10):
        """Checks whether the item has been loaded in the specified time."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            log.info("Page was load")
            return True

        except TimeoutException:
            log.warning(f"Element not found: {value} (Waited {timeout}s)")
            return False

    def _set_proxy(self):
        self.seleniumwire_options["proxy"] = {
            "http": config.get_proxy["http"],
            "https": config.get_proxy["https"],
            "no_proxy": config.get_proxy["no_proxy"],
        }

    def _modify_headers(self, request):
        for url, headers in config.get_headers.items():
            if url in request.url:
                for key, value in headers.items():
                    request.headers[key] = value
